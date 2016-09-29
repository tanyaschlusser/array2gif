Array2GIF: utility to convert NumPy arrays to (animated) GIF 89a format
=======================================================================

.. figure:: https://tanyaschlusser.github.io/ising/img/ising_animation_1.6.gif
    :alt: Animation of random pixels converging from two colors to one color.
    :width: 30%

    An animated GIF showing a Monte Carlo simulation to obtain an equilibrium
    magetization, using the Ising model, at T / T_{critical} = 70%.


.. figure:: https://tanyaschlusser.github.io/ising/img/ising_animation_2.0.gif
    :alt: Animation of random pixels converging less slowly to one color.
    :width: 30%

    An animated GIF showing a Monte Carlo simulation to obtain an equilibrium
    magetization, using the Ising model, at T / T_{critical} = 88%.


.. figure:: https://tanyaschlusser.github.io/ising/img/ising_animation_2.4.gif
    :alt: Animation of random pixels staying mostly random.
    :width: 30%

    An animated GIF showing a Monte Carlo simulation to obtain an equilibrium
    magetization, using the Ising model, at T / T_{critical} = 106% ...
    staying random because now the influence of temperature exceeds the
    coupling force between atoms.


Array2GIF provides a single top-level function, `write_gif()`, to
write a 3-D NumPy array to a GIF, or a list of these arrays to an
animated GIF.

It is currently in alpha stage, with no attempt at optimization for
speed, but it works great for me -- just small animations of thermodynamics
simulations, like the magnetization in the Ising model shown here.


Usage
-----

Here is an example for a 2 pixel by 3 pixel animated GIF with
two frames, switching 5 frames per second. All animations from this
library will loop indefinitely.

::

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



Installation
------------

It's not on PyPI yet, so: ::

    pip install git+https://github.com/tanyaschlusser/array2gif.git#egg=array2gif


.. _`the repository`: http://github.com/tanyaschlusser/array2gif
