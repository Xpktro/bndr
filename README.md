Bndr
====

This package is basically two things:

* A library for creating glitch art in the form of [Databending](https://en.wikipedia.org/wiki/Databending) via a simple filter chain for the raw input image data. You can manipulate any jpeg/png image file using the builtin filters or construct your own filters.
* A CLI for generating databended images using random a random filter arrangement (and an optional seed value to produce predictable results).


### Requirements

Bndr requires the `Pillow` package (with zlib and libjpeg support). In most cases you would only need to install `libjpeg` and `zlib` system packages since pip installation will deal with Pillow. Please search for instructions on how to install these packages for your OS (there are *plenty* of resources for this across the internet) by yourself.


### Installation

You can install this package from pip simply by running:

    pip install bndr

Or if you clone the source code repository by running:

    python setup.py install


### Bndr CLI

The Bndr CLI is made up of two commands:

* `bndrimg` - Image conversion a random filter chain or and an optional seed.

    **Parameters:**

    * `input` (positional, mandatory): Location of input image. Must be a jpeg or png image.
    * `-o --output`(optional): Location of the output file. If not supplied, will default to `(input filename)_out.png`. Always produces a png image file.
    * `-s --seed` (optional): Seed for generating a specific filter chain. Can be any string or number.
    
    **Usage Examples:**

    Generate a random glitched image given an input called `input.jpg`:

        bndrimg input.jpg

    Generate a random glitched image (named `output.png`) given an input called `input.jpg`:
    
        bndrimg input.jpg -o output.png

    Generate a glitched image given an input called `input.jpg` with a seed value of `value`:
        
        bndrimg input.jpg -s value

* `bndrtxt` - Simple utility to generate random-case and random-symbol-replace texts.

    **Parameters:**

    * `input` (positional, mandatory): Text to be *bent*.
    
    **Usage Examples:**
    
    Bend the string `Hello world.`:

        bndrtxt "Hello world."


### Bndr Library

#### Quickstart

As mentioned in the introduction, Bndr works chaining a series of filters applied to the raw (binary) image data in order to *bend* it. Let's say, for example, that you want to apply the `ADRNBend` filter to an image and save it's results:

```python
from bndr import Bndr, ADRNBend

with open('input.jpg', 'rb') as input_image:
    bndr = Bndr(input_image.read())
    with open('output.jpg', 'wb') as output_image:
        output_data = bndr.process(ADRNBend())
        output_image.write(output_data)
```

This is a simplified version of what the `bndrimg` command does, since some chained filters configurations can severely damage an image and the input image wont be a jpg all times.

Some filters accept configuration values as positional or named arguments, and the `Bndr.process` function can receive an undefined number of filters as arguments to work (it will apply the filters in order of declaration). For example, to apply a 90 degree rotation (via the `Rotate` filter) prior to the `ADRNBend` filter, we would replace the `output_data` assignation with:

```python
from bndr import Bndr, ADRNBend, Rotate

# ...

output_data = bndr.process(Rotate(90), ADRNBend())
```

Currently, Bndr bundles the following list of filters:

* `bndr.ADRNBend(amount=5)`
A databend filter that replaces bytes in the `a-e` range randomly.
    * **`amount`** - Number of times to repeat the replace operation.

* `bndr.ChrisBend(amount=5)`
A databend filter that adds random repeated byte chunks from the same image.
    * **`amount`** - Number of times to repeat the chunk addition operation.

* `bndr.JpglitchBend(amount=randint(0, 99), seed=randint(0, 99), iterations=randint(0, 115))`
A databend filter that replaces random bytes from the image into arbitrary values.
    * **`amount`** - Value to replace into the file.
    * **`seed`** - Value used to fine-tune the positions to be replaced into the file.
    * **`iterations`** - Number of times the replacement operation will be repeated.

* `bndr.ADRNGrayscale()`
An image filter that converts the image into black and white.

* `bndr.Blur()` 
A filter that blurs the input image using a Gaussian blur.

* `bndr.Rotate([amount=choice((0, 90, 180, 270, 360))])` 
A filter that rotates the input image by a given amount which defaults to a random from the group (0, 90, 180, 270, 360)).

* `bndr.Sharpness([factor=random() * 2])`
A filter that enhaces or blurs the edges of the input image by a given factor. A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image, and a factor of 2.0 gives a sharpened image.

* `bndr.Desaturate([factor=random()])`
A filter that desaturates the input image colors based on a given factor. A factor of 0.0 gives a black and white image. A factor of 1.0 gives the original image.

* `bndr.Min()`
A filter that picks the lowest pixel value in a matrix of 3x3 surrounding every pixel in the image.

* `bndr.Max()`
A filter that picks the largest pixel value in a matrix of 3x3 surrounding every pixel in the image.

* `bndr.Median()`
A filter that picks the median pixel value in a matrix of 3x3 surrounding every pixel in the image.

#### Bndr API

Bndr is designed (which is a pretentious thing to say, since it's *very* simple) to make your writing of databending filters as unobstrusive as possible since it's nanometric-scale api is composed of three classes:


#### `class bndr.Bndr(image)`
Creates an instance of this class for the given raw image data.

* **`image`** - Raw image data. Must be a bytestring, as a result of a binary file read or similar. Images must are expected to be JPEGs. After the creation of the `Bndr` instance, this data will be available as the instance member `self.image`. 

##### `Bndr.process(*filters)`
Applies the filter chain to the given instance.

* **`*filters`** - List of filters to apply, filters must be sub-instances of `BndrFilter`. Returns the raw image data of the filtered image.


#### `class bndr.BndrFilter(*args, **kwargs)`
Creates an instance of this filter for the given arguments and keyword arguments.

* **`*args`** - Positional, optional arguments that will be available upon creation as the instance member `self.args`.
* **` **kwargs `** - Named, optional arguments that will be available upon creation as the instance member `self.kwargs`.

##### `BndrFilter.process(image)`
Handler for image filtering. Must return a bytestring of the (filtered) input image data.

* **`image`** - Raw image data. Must be a bytestring, as a result of a binary file read or similar.


#### `class bndr.PILBndrFilter(*args, **kwargs)`
Creates an instance of this filter for the given arguments and keyword arguments. This is an utility class that wraps the raw image data into a Pillow Image instance.

* **`*args`** - Positional, optional arguments that will be available upon creation as the instance member `self.args`.
* **` **kwargs `** - Named, optional arguments that will be available upon creation as the instance member `self.kwargs`.

##### `PILBndrFilter.process_img(image)`
Handler for image filtering. Must return a Pillow Image instance.

* **`image`** - Image data in the form of a Pillow Image instance.
