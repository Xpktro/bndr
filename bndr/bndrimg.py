# coding:utf-8
import argparse
import random
import six

from PIL import Image

if six.PY2:
    from cStringIO import StringIO
else:
    from io import BytesIO as StringIO

from .bndr import Bndr
from .filters import Blur, Sharpness, Desaturate, Min, Max, Median, \
    ADRNGrayscale, Rotate, ADRNBend, ChrisBend, JpglitchBend


def random_filters(seed=None):
    if seed:
        random.seed(seed)
    filters = []

    if random.randint(1, 5) == 1:
        filters.append(Blur())

    if random.randint(1, 7) == 1:
        filters.append(Sharpness())

    if random.randint(1, 4) == 1:
        filters.append(Desaturate())

    if random.randint(1, 10) == 1:
        filters.append(Min())

    if random.randint(1, 10) == 1:
        filters.append(Max())

    if random.randint(1, 10) == 1:
        filters.append(Median())

    if random.randint(1, 30) == 1:
        filters.append(ADRNGrayscale())

    filters = list(filter(lambda i: random.randint(1, 10) == 1, filters))

    for _ in range(random.randint(0, 3)):
        if random.randint(1, 7) <= 2:
            amount = random.choice((0, 45, 90, 135, 180, 225, 270, 315, 360))
            amount = amount * -1 if random.choice((True, False)) else amount
            filters.append(Rotate(amount))
            filters.append(Rotate(amount * -1))

    for _ in range(random.randint(1, 3)):
        filters.append(random.choice([
            ADRNBend(amount=random.randint(3, 20)),
            ChrisBend(amount=random.randint(3, 20)),
            JpglitchBend()
        ]))

    random.shuffle(filters)
    return filters


def output_filename(input_filename):
    filename, extension = input_filename.split('.')
    return '{}_out.png'.format(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input image')
    parser.add_argument('-o', '--output', required=False, help='output image')
    parser.add_argument('-s', '--seed', default='', help='seed')
    args = parser.parse_args()

    with open(args.input, 'rb') as input_image:
        jpg_output = StringIO()
        Image.open(input_image).save(jpg_output, format='JPEG', quality=100)
        jpg_output.seek(0)
        bndr = Bndr(jpg_output.read())
        output = args.output or output_filename(args.input)
        with open(output, 'wb') as output_image:
            while True:
                try:
                    filters = random_filters(args.seed)
                    Image.open(StringIO(bndr.process(*filters)))\
                         .save(output_image, format='PNG')
                    break
                except:
                    continue


if __name__ == '__main__':
    main()
