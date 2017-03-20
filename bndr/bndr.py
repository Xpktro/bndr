# coding:utf-8
import six
from PIL import Image

if six.PY2:
    from cStringIO import StringIO
else:
    from functools import reduce
    from io import BytesIO as StringIO

__all__ = ['Bndr', 'BndrFilter', 'PILBndrFilter']


class Bndr(object):
    def __init__(self, image):
        self.image = image

    def process(self, *filters):
        return reduce(lambda image, f: f(image), filters, self.image)


class BndrFilter(object):
    def __init__(self, *args, **kwargs):
        self.args = args or []
        self.kwargs = kwargs or {}

    def __call__(self, image):
        return self.process(image)

    def process(self, image):
        raise NotImplementedError


class PILBndrFilter(BndrFilter):
    def __call__(self, image):
        self.image = Image.open(StringIO(image))
        self.format = self.image.format
        return super(PILBndrFilter, self).__call__(image)

    def process(self, image):
        self.image = self.process_img(self.image)
        output_str = StringIO()
        self.image.save(output_str,
                        format='JPEG', quality=95)
        output_str.seek(0)
        return output_str.read()

    def process_img(self, image):
        raise NotImplementedError
