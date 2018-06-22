.. :changelog:

Release History
---------------


1.0.4 (2018-06-22)
++++++++++++++++++

**Bugfixes**

- Fixed issue where error was raised when non-integer dataset
  is used: instead now it is cast to `uint8` and a warning is
  raised if there's a difference between the two images.

- Addressed issue where no error is raised when there are
  more colors than possible in a GIF (256 max). Although
  it is possible to have a separate palette for every
  single frame, this is not implemented right now, and
  the initial global palette is used for the entire animation.

1.0.3 (2018-06-02)
++++++++++++++++++

**Bugfixes**

- Did not bump version in documentation last times.

1.0.1 (2018-06-02)
++++++++++++++++++

**Bugfixes**

- Fixed issue where the width and height of an image are swapped.
  This is clear in image editors but was not obvious when viewed
  in Chrome.


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
