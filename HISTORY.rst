.. :changelog:

Release History
---------------


1.0.0 (2018-05-23)
++++++++++++++++++

**Improvements**

- It is now possible to use PIL ordering of data (rows x cols x rgb) 
  in addition to the original ordering (rgb x rows x cols).

**Bugfixes**

- Fixed issue where array2gif would raise ``ValueError`` when using
  a 4D NumPy array with perfectly valid data. Now it is possible to
  use either a list of 3D NumPy arrays, or a 4D NumPy array for
  animated gifs.


0.1.0 (2016-09-30)
++++++++++++++++++

**Initial release**

- One single function, ``write_gif``.
