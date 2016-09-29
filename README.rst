Array2GIF: convert NumPy arrays to (animated) GIF
=================================================


 +-------------+--------------+--------------+
 | |ising1|    + |ising2|     + |ising3|     +
 | T = 0.7 T_c + T = 0.88 T_c + T = 1.06 T_c +
 +-------------+--------------+--------------+


These are animated GIFs showing a Monte Carlo simulation to obtain a distribution
of equilibrium magnetization, using the Ising model, at various dimensionless temperatures
relative to the Curie temperature. It explores the interplay between the magnetic
coupling force between atoms, and the randomness from the temperature.


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
.. |ising1| image:: https://tanyaschlusser.github.io/ising/img/ising_animation_1.6.gif
   :width: 30%
   :align: middle
   :alt: Animation of random pixels converging from two colors to one color. T = 0.7 T_c.
.. |ising2| image:: https://tanyaschlusser.github.io/ising/img/ising_animation_2.0.gif
   :width: 30%
   :align: middle
   :alt: Animation of random pixels converging less slowly to one color. T = 0.88 T_c.
.. |ising3| image:: https://tanyaschlusser.github.io/ising/img/ising_animation_2.4.gif
   :width: 30%
   :align: middle
   :alt: Animation of random pixels staying mostly random. T = 1.06 T_c.
