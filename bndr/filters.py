# coding:utf-8
import copy
import random
import six

if six.PY2:
    from itertools import izip, tee
    from cStringIO import StringIO
else:
    from io import BytesIO as StringIO
    from itertools import tee
    izip = zip
    xrange = range

from PIL import Image, ImageFilter, ImageEnhance

from .bndr import BndrFilter, PILBndrFilter


__all__ = ['ADRNBend', 'ChrisBend', 'JpglitchBend', 'ADRNGrayscale', 'Blur',
           'Rotate', 'Sharpness', 'Desaturate', 'Min', 'Max', 'Median']


class ADRNBend(BndrFilter):
    """Based on databend.py from adrn https://gist.github.com/adrn/4090186"""

    def process(self, image):
        header = image[:1000]
        core_data = image[1000:]
        data_size = len(core_data)

        letters = 'abcde'
        for _ in range(self.kwargs.get('amount', 5)):
            ii = random.randint(0, data_size - 1)
            jj = random.randint(ii, ii + random.randint(100, 10000))

            pre = core_data[:ii]
            post = core_data[jj:]
            sub_data = core_data[ii:jj]
            sub_data = sub_data.replace(random.choice(letters),
                                        random.choice(letters))

            core_data = pre + sub_data + post
        return header + core_data


class ChrisBend(BndrFilter):
    """Based on an article from Chris Cuellar:
    http://blog.art21.org/2011/09/20/how-to-use-python-to-create-a-simple-flickr-photo-glitcher"""

    def process(self, image):
        image_processed = image[:]
        for i in range(self.kwargs.get('amount', 5)):
            image_processed = self.splice_a_chunk_in_a_file(image_processed)
        return image_processed

    def splice_a_chunk_in_a_file(self, file_data):
        start_point, end_point = \
            self.get_random_start_and_end_points_in_file(file_data)
        section = file_data[start_point:end_point]
        repeated = ''

        for i in range(1, random.randint(1, 5)):
            repeated += section

        new_start_point, new_end_point = \
            self.get_random_start_and_end_points_in_file(file_data)
        file_data = file_data[:new_start_point] + repeated + \
                    file_data[new_end_point:]
        return file_data

    def get_random_start_and_end_points_in_file(self, file_data):
        start_point = random.randint(2500, len(file_data))
        end_point = start_point + \
                    random.randint(0, len(file_data) - start_point)

        return start_point, end_point


class JpglitchBend(BndrFilter):
    """Based on jpglitch.py from https://github.com/Kareeeeem/jpglitch"""
    def process(self, image):
        while True:
            new_bytes = self.glitch_bytes(image)
            try:
                im = Image.open(StringIO(new_bytes))
                im.save(StringIO(), format='JPEG', quality=100)
                return new_bytes
            except IOError:
                pass

    def glitch_bytes(self, image):
        """Glitch the image bytes, after the header based on the parameters.
        'Amount' is the hex value that will be written into the file. 'Seed'
        tweaks the index where the value will be inserted, rather than just a
        simple division by iterations. 'Iterations' should be self explanatory
        """

        amount = self.kwargs.get('amount', random.randint(0, 99)) / 100
        seed = self.kwargs.get('seed', random.randint(0, 99)) / 100
        iterations = self.kwargs.get('iterations', random.randint(0, 115))
        header_length = self.get_header_length(image)

        # work with a copy of the original bytes. We might need the original
        # bytes around if we glitch it so much we break the file.
        new_bytes = bytearray(copy.copy(image))

        for i in (xrange(iterations)):
            max_index = len(image) - header_length - 4

            # The following operations determine where we'll overwrite a value
            # Illustrate by example

            # 36 = (600 / 50) * 3
            px_min = int((max_index / iterations) * i)

            # 48 = (600 / 50) * 3 + 1
            px_max = int((max_index / iterations) * (i + 1))

            # 12 = 48 - 36
            delta = (px_max - px_min)  # * 0.8

            # 36 + (12 * 0.8)
            px_i = int(px_min + (delta * seed))

            # If the index to be changed is beyond bytearray length file set
            # it to the max index
            if px_i > max_index:
                px_i = max_index

            byte_index = header_length + px_i
            new_bytes[byte_index] = int(amount * 256)

        return new_bytes

    def pairwise(self, iterable):
        """Awesome function from the itertools cookbook
        https://docs.python.org/2/library/itertools.html
        s -> (s0,s1), (s1,s2), (s2, s3), ...
        """
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)

    def get_header_length(self, image):
        """Get the length of the header by searching sequential 0xFF 0xDA
        values. These values mark the end of a Jpeg header. We add two to give
        us a little leeway. We don't want to mess with the header.
        """

        for i, pair in enumerate(self.pairwise(image)):
            if pair[0] == 255 and pair[1] == 218:
                result = i + 2
                return result

        # Fallback from ADRNBend, original raised an exception
        return 1000


class ADRNGrayscale(PILBndrFilter):
    """Based on databend.py from adrn https://gist.github.com/adrn/4090186"""
    def process_img(self, image):
        return image.convert('1')


class Blur(PILBndrFilter):
    def process_img(self, image):
        return image.filter(ImageFilter.GaussianBlur())


class Rotate(PILBndrFilter):
    def process_img(self, image):
        if len(self.args) > 0:
            amount = self.args[0]
        else:
            amount = random.choice((0, 90, 180, 270, 360))
        return image.rotate(amount)


class Sharpness(PILBndrFilter):
    def process_img(self, image):
        if len(self.args) > 0:
            factor = self.args[0]
        else:
            factor = random.random() * 2
        return ImageEnhance.Sharpness(image).enhance(factor)


class Desaturate(PILBndrFilter):
    def process_img(self, image):
        if len(self.args) > 0:
            factor = self.args[0]
        else:
            factor = random.random()
        return ImageEnhance.Color(image).enhance(factor)


class Min(PILBndrFilter):
    def process_img(self, image):
        return image.filter(ImageFilter.MinFilter)


class Max(PILBndrFilter):
    def process_img(self, image):
        return image.filter(ImageFilter.MaxFilter)


class Median(PILBndrFilter):
    def process_img(self, image):
        return image.filter(ImageFilter.MedianFilter)
