"""
array2gif.core
~~~~~~~~~~~~~~

Defines the function `write_gif()`, with helper functions
to create the internal blocks required for the GIF 89a format.


Implements the definition of GIF 89a in:
https://www.w3.org/Graphics/GIF/spec-gif89a.txt,
which was made understandable by Matthew Flickinger's blog:
http://www.matthewflickinger.com/lab/whatsinagif/bits_and_bytes.asp
"""
from __future__ import division
import math
import struct
from collections import Counter

import numpy


BLOCK_TERMINATOR = b'\x00'
EXTENSION = b'\x21'
HEADER = b'GIF89a'
TRAILER = b'\x3b'
ZERO = b'\x00'


def little_end(number, length=2):
    return struct.pack('<I', number)[:length]


def check_dataset_range(dataset):
    """Confirm no rgb value is outside the range [0, 255]."""
    if dataset.max() > 255 or dataset.min() < 0:
        raise ValueError('The dataset has a value outside the range [0,255]')


def check_dataset_shape(dataset):
    """Confirm the dataset has shape 3 x nrows x ncols."""
    if len(dataset.shape) != 3:
        raise ValueError('The dataset needs 3 dimensions: rgb, nrows, ncols')
    if dataset.shape[0] != 3:
        raise ValueError(
            'The dataset\'s first dimension must have all 3\n'
            'colors: red, green, and blue...in that order.'
        )


def check_dataset(dataset):
    """Confirm shape (3 colors x rows x cols) and values [0 to 255] are OK."""
    if isinstance(dataset, numpy.array):
        check_dataset_shape(dataset)
        check_dataset_range(dataset)
    else:  # must be a list of arrays
        for i, d in enumerate(dataset):
            if not isinstance(d, numpy.array):
                raise ValueError(
                    'Requires a NumPy array (rgb x rows x cols) '
                    'with integer values in the range [0, 255].'
                )
            try:
                check_dataset_shape(dataset)
                check_dataset_range(dataset)
            except ValueError as err:
                raise ValueError(
                    '{}\nAt position {} in the list of arrays.'
                    .format(err, i)
                )


def get_image(dataset):
    """Convert the NumPy array to two nested lists with r,g,b tuples."""
    dim, nrow, ncol = dataset.shape
    image = [[
            b''.join(
                little_end(dataset[k, i, j], length=1)
                for k in range(dim)
            )
            for j in range(ncol)]
        for i in range(nrow)]
    return image


# -------------------------------- Logical Screen Descriptor --- #
def get_color_table_size(num_colors):
    """Total values in the color table is 2**(1 + int(result, base=2)).

    The result is a three-bit value (represented as a string with
    ones or zeros) that will become part of a packed byte encoding
    various details about the color table, used in the Logical
    Screen Descriptor block.
    """
    nbits = max(math.ceil(math.log(num_colors, 2)), 2)
    return '{:03b}'.format(int(nbits - 1))


def _get_logical_screen_descriptor(image, colors):
    w = len(image)
    h = len(image[0])
    width = little_end(w)
    height = little_end(h)
    global_color_table_flag = '1'
    # color resolution possibly doesn't do anything, because
    # the size of the colors in the global color table is always
    # 6 bytes (e.g. 0xFFFFFF) per color, and bits needed to express
    # the total number of colors is expressly stated at the beginning
    # of the LZW compression (later). Flickinger says to just use '001'
    color_resolution = '001'
    colors_sorted_flag = '0'  # even though I try to sort
    size_of_global_color_table = get_color_table_size(len(colors))
    packed_bits = little_end(
        int(
            global_color_table_flag +
            color_resolution +
            colors_sorted_flag +
            size_of_global_color_table,
            base=2
        ),
        length=1
    )
    background_color_index = ZERO
    pixel_aspect_ratio = b'\x00'
    logical_screen_descriptor = b''.join((
        width,
        height,
        packed_bits,
        background_color_index,
        pixel_aspect_ratio
    ))
    return logical_screen_descriptor


# --------------------------------------- Global Color Table --- #
def get_colors(image):
    """Return a Counter containing each color and how often it appears.
    """
    colors = Counter(pixel for row in image for pixel in row)
    return colors


def _get_global_color_table(colors):
    """Return a color table sorted in descending order of count.
    """
    global_color_table = b''.join(c[0] for c in colors.most_common())
    full_table_size = 2**(1+int(get_color_table_size(len(colors)), 2))
    zeros = b''.join(ZERO * 3 for i in range(full_table_size - len(colors)))
    return global_color_table + zeros


# ------------------------------- Graphics Control Extension --- #
def _get_graphics_control_extension(delay_time=0):
    control_label = b'\xf9'
    block_size = little_end(4, length=1)
    disposal_method = '001'
    user_input_expected = '0'
    transparent_index_given = '0'
    packed_bits = little_end(
        int(
            '000' +
            disposal_method +
            user_input_expected +
            transparent_index_given,
            base=2
        ),
        length=1
    )
    delay_time = little_end(delay_time)
    transparency_index = ZERO
    graphics_control_extension = b''.join((
        EXTENSION,
        control_label,
        block_size,
        packed_bits,
        delay_time,
        transparency_index,
        BLOCK_TERMINATOR
    ))
    return graphics_control_extension


# ----------------------------------- Application Extension --- #
def _get_application_extension(loop_times=0):
    ANIMATION_LABEL = b'\xff'
    block_size = little_end(11, length=1)
    application_identifier = b'NETSCAPE2.0'
    data_length = little_end(3, length=1)
    loop_value = little_end(loop_times, length=2)
    application_extension = b''.join((
        EXTENSION,
        ANIMATION_LABEL,
        block_size,
        application_identifier,
        data_length,
        b'\x01',
        loop_value,
        BLOCK_TERMINATOR
    ))
    return application_extension


# -============================================ Image Block =====- #
# --------------------------------------- Image Descriptor --- #
def _get_image_descriptor(image, left=0, top=0):
    image_separator = b'\x2c'
    image_left_position = little_end(left)
    image_top_position = little_end(top)
    image_width = little_end(len(image[0]))
    image_height = little_end(len(image))
    local_color_table_exists = '0'
    interlaced_flag = '0'
    sort_flag = '0'
    reserved = '000'
    local_color_table_size = '000'
    packed_bits = little_end(
        int(
            local_color_table_exists +
            interlaced_flag +
            sort_flag +
            reserved +
            local_color_table_size,
            base=2
        ),
        length=1
    )
    image_descriptor = b''.join((
        image_separator,
        image_left_position,
        image_top_position,
        image_width,
        image_height,
        packed_bits
    ))
    return image_descriptor


# --------------------------------------------- Image Data --- #
def _get_image_data(image, colors):
    """Performs the LZW compression as described by Matthew Flickinger.

    This isn't fast, but it works.
    http://www.matthewflickinger.com/lab/whatsinagif/lzw_image_data.asp
    """
    MAX_COMPRESSION_CODE = 4095
    base_lookup = dict((c[0], i) for i, c in enumerate(colors.most_common()))
    lookup = base_lookup.copy()
    lzw_code_size = int(get_color_table_size(len(colors)), 2) + 1
    clear_code = 2**lzw_code_size
    end_code = clear_code + 1
    next_compression_code = end_code
    # Get the minimum number of bits needed for the next code.
    nbits = len('{:b}'.format(next_compression_code))
    pixel_stream = [pixel for row in image for pixel in row]
    pixel_buffer = [pixel_stream.pop(0)]
    coded_bits = [(clear_code, nbits)]
    for pixel in pixel_stream:
        test_string = b''.join(pixel_buffer) + pixel
        if test_string in lookup:
            pixel_buffer.append(pixel)
        elif next_compression_code >= MAX_COMPRESSION_CODE:
            coded_bits.insert(0, (lookup[b''.join(pixel_buffer)], nbits))
            coded_bits.insert(0, (clear_code, nbits))
            pixel_buffer = [pixel]
            next_compression_code = end_code
            nbits = len('{:b}'.format(next_compression_code))
        else:
            code = lookup[b''.join(pixel_buffer)]
            coded_bits.insert(0, (code, nbits))
            pixel_buffer = [pixel]
            next_compression_code += 1
            nbits = len('{:b}'.format(next_compression_code))
            lookup[test_string] = next_compression_code
    # Add the last content from the pixel buffer.
    coded_bits.insert(0, (lookup[b''.join(pixel_buffer)], nbits))
    coded_bits.insert(0, (end_code, nbits))
    coded_bytes = ''.join(
        '{{:0{}b}}'.format(vbits).format(val) for val, vbits in coded_bits)
    coded_bytes = '0' * ((8 - len(coded_bytes)) % 8) + coded_bytes
    coded_data = list(
        reversed([
            int(coded_bytes[8*i:8*(i+1)], 2)
            for i in range(len(coded_bytes) // 8)
        ])
    )
    output = little_end(lzw_code_size, length=1)
    # Must output the data in blocks of length 255
    block_length = min(255, len(coded_data))
    while block_length > 0:
        block = b''.join(
            little_end(code, length=1) for code in coded_data[:block_length]
        )
        output = (
            output +
            little_end(block_length, length=1) +
            block
        )
        coded_data = coded_data[block_length:]
        block_length = min(255, len(coded_data))
    return output


def _get_sub_image(image, colors, delay_time=0):
    graphics_control_extension = (
        _get_graphics_control_extension(delay_time=delay_time)
    )
    image_descriptor = _get_image_descriptor(image)
    image_data = _get_image_data(image, colors)
    return b''.join((
        graphics_control_extension,
        image_descriptor,
        image_data,
        BLOCK_TERMINATOR))


def _make_gif(dataset):
    image = get_image(dataset)
    colors = get_colors(image)
    yield _get_logical_screen_descriptor(image, colors)
    yield _get_global_color_table(colors)
    yield _get_sub_image(image, colors)


def _make_animated_gif(datasets, delay_time=10):
    images = [get_image(d) for d in datasets]
    color_sets = (get_colors(image) for image in images)
    colors = Counter()
    for color_set in color_sets:
        colors += color_set
    yield _get_logical_screen_descriptor(images[0], colors)
    yield _get_global_color_table(colors)
    yield _get_application_extension()
    for image in images:
        yield _get_sub_image(image, colors, delay_time=delay_time)


def write_gif(dataset, filename, fps=10):
    """Write a NumPy array to GIF 89a format.

    Or write a list of NumPy arrays to an animation (GIF 89a format).

    - Positional arguments::

        :param dataset: A NumPy arrayor list of arrays with shape
                        rgb x rows x cols and integer values in [0, 255].
        :param filename: The output file that will contain the GIF image.
        :param fps: The (integer) frames/second of the animation (default 10).
        :type dataset: a NumPy array or list of NumPy arrays.
        :return: None

    - Example: a minimal array, with one red pixel, would look like this::

        import numpy as np
        one_red_pixel = np.array([[[255]], [[0]], [[0]]])
        write_gif(one_red_pixel, 'red_pixel.gif')

    ..raises:: ValueError
    """
    check_dataset(dataset)
    delay_time = 100 // int(fps)

    def encode(d):
        if isinstance(d, list):
            return _make_animated_gif(d, delay_time=delay_time)
        else:
            return _make_gif(d)

    with open(filename, 'wb') as outfile:
        outfile.write(HEADER)
        for block in encode(dataset):
            outfile.write(block)
        outfile.write(TRAILER)