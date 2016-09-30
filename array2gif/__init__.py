"""
array2gif
~~~~~~~~~

Convert a NumPy array with shape (rgb x nrows x ncols) to GIF 89a format,
or a list of NumPy arrays to an animated GIF.


Here's a full example for a 2 pixel by 3 pixel animated
GIF with two frames::

    import numpy as np
    from array2gif import write_gif

    dataset = [
        np.array([
            [[255, 0, 0], [255, 0, 0]],  # red intensities
            [[0, 255, 0], [0, 255, 0]],  # green intensities
            [[0, 0, 255], [0, 0, 255]]   # blue intensities
        ]),
        np.array([
            [[0, 0, 255], [0, 0, 255]],
            [[0, 255, 0], [0, 255, 0]],
            [[255, 0, 0], [255, 0, 0]]
        ])
    ]

    write_gif(dataset, "output.gif", fps=5)

The three dimensions must be the integer color intensities from
0-255 for red, green, and blue -- in that order. The two frames
are:

    red  green  blue
    red  green  blue

    and

    blue green  red
    blue green  red

"""
from array2gif.core import check_dataset, write_gif
