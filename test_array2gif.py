#!/usr/bin/env python

"""Tests for array2gif."""

import os
import unittest
import warnings
import numpy as np
import array2gif.core as core
from collections import Counter


class Array2GIFTestCase(unittest.TestCase):
    """Array2GIF test cases."""

    def setUp(self):
        self.filename = 'array2gif_test.gif'
        self.flickinger_dataset = np.array([
            [
                [255, 255, 255, 255, 255,   0,   0,   0,   0,   0],
                [255, 255, 255, 255, 255,   0,   0,   0,   0,   0],
                [255, 255, 255, 255, 255,   0,   0,   0,   0,   0],
                [255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
                [255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
                [0,     0,   0, 255, 255, 255, 255, 255, 255, 255],
                [0,     0,   0, 255, 255, 255, 255, 255, 255, 255],
                [0,     0,   0,   0,   0, 255, 255, 255, 255, 255],
                [0,     0,   0,   0,   0, 255, 255, 255, 255, 255],
                [0,     0,   0,   0,   0, 255, 255, 255, 255, 255]
            ],
            [
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                [0,   0,   0, 255, 255, 255, 255,   0,   0,   0],
                [0,   0,   0, 255, 255, 255, 255,   0,   0,   0],
                [0,   0,   0, 255, 255, 255, 255,   0,   0,   0],
                [0,   0,   0, 255, 255, 255, 255,   0,   0,   0],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
            ],
            [
                [0,     0,   0,   0,   0, 255, 255, 255, 255, 255],
                [0,     0,   0,   0,   0, 255, 255, 255, 255, 255],
                [0,     0,   0,   0,   0, 255, 255, 255, 255, 255],
                [0,     0,   0, 255, 255, 255, 255, 255, 255, 255],
                [0,     0,   0, 255, 255, 255, 255, 255, 255, 255],
                [255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
                [255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
                [255, 255, 255, 255, 255,   0,   0,   0,   0,   0],
                [255, 255, 255, 255, 255,   0,   0,   0,   0,   0],
                [255, 255, 255, 255, 255,   0,   0,   0,   0,   0]
            ]
        ])
        self.flickinger_image = core.get_image(self.flickinger_dataset)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_range_error_when_out_of_bounds(self):
        with self.assertRaises(ValueError):
            d = np.array([[[0]], [[-1]], [[0]]])
            core.check_dataset_range(d)
        with self.assertRaises(ValueError):
            d = np.array([[[0]], [[256]], [[0]]])
            core.check_dataset_range(d)

    def test_no_range_error_when_in_bounds(self):
        d = np.array([[[1]], [[1]], [[255]]])
        try:
            core.check_dataset_range(d)
        except ValueError:
            msg = "`check_dataset_range` raised ValueError on allowed color."
            self.fail(msg)

    def test_shape_error_when_not_3d(self):
        with self.assertRaises(ValueError):
            d = np.array([[0], [0], [0]])
            core.check_dataset_shape(d)
        with self.assertRaises(ValueError):
            d = np.array([[[0]], [[0]]])
            core.check_dataset_shape(d)
        with self.assertRaises(ValueError):
            d = np.array([[[0]], [[0]], [[0]], [[0]]])
            core.check_dataset_shape(d)

    def test_no_shape_error_when_4d_numpy_array(self):
        one_red_pixel = np.array([[[255]], [[0]], [[0]]])
        one_green_pixel = np.array([[[0]], [[255]], [[0]]])
        d = np.array([one_red_pixel, one_green_pixel])
        try:
            core.check_dataset(d)
        except ValueError as e:
            msg = "`check_dataset` ValueError on 4D numpy array.\n{}"
            self.fail(msg.format(e))

    def test_fix_shape_error_when_PIL_format(self):
        one_green_pixel = np.array([[[0]], [[255]], [[0]]])
        pil_green_pixel = np.array([[[0, 255, 0]]])
        with self.assertRaises(ValueError):
            core.check_dataset(pil_green_pixel)
        d = core.try_fix_dataset(pil_green_pixel)
        try:
            core.check_dataset(d)
        except ValueError as e:
            msg = "`check_dataset` ValueError on fixed dataset.\n{}"
            self.fail(msg.format(e))
        self.assertEqual(True, (d == one_green_pixel).all())

    def test_fix_shape_error_when_PIL_format_in_4d_numpy_array(self):
        one_red_pixel = np.array([[[255]], [[0]], [[0]]])
        one_green_pixel = np.array([[[0]], [[255]], [[0]]])
        d = np.array([one_red_pixel, one_green_pixel])
        pil_d = np.array([one_red_pixel.transpose(), one_green_pixel.transpose()])
        with self.assertRaises(ValueError):
            core.check_dataset(pil_d)
        fixed_d = core.try_fix_dataset(pil_d)
        try:
            core.check_dataset(fixed_d)
        except ValueError as e:
            msg = "`check_dataset` ValueError on fixed 4D dataset.\n{}"
            self.fail(msg.format(e))
        self.assertEqual(True, (fixed_d == d).all())

    def test_warning_on_non_uint8_dataset(self):
        d = np.array([[[1]], [[2]], [[3.14]]])
        with warnings.catch_warnings(record=True) as wlist:
            core.get_image(d)
            self.assertTrue(len(wlist) > 0)
            self.assertTrue(any('array2gif' in w.filename for w in wlist))

    def test_warning_on_non_uint8_dataset(self):
        d = np.array([[[1]], [[2]], [[3]]])
        with warnings.catch_warnings(record=True) as wlist:
            core.get_image(d)
            self.assertEqual(len(wlist), 0)

    def test_pixels_three_bytes(self):
        d = np.array([[[1]], [[2]], [[3]]])
        img = core.get_image(d)
        self.assertEqual(len(img[0][0]), 3)

    def test_pixels_in_order(self):
        d = np.array([[[1]], [[2]], [[3]]])
        img = core.get_image(d)
        self.assertEqual(img[0][0], b'\x01\x02\x03')

    def test_min_color_table_size_is_two(self):
        binary_string_table_size = core.get_color_table_size(2)
        self.assertEqual(int(binary_string_table_size, base=2), 1)

    def test_color_table_size(self):
        binary_string_table_size = core.get_color_table_size(15)
        self.assertEqual(int(binary_string_table_size, base=2), 3)

    def test_get_colors(self):
        colors = core.get_colors(self.flickinger_image)
        self.assertEqual(
            colors,
            Counter(
                {b'\xff\x00\x00': 42, b'\x00\x00\xff': 42, b'\xff\xff\xff': 16}
            )
        )

    def test_logical_screen_descriptor(self):
        colors = core.get_colors(self.flickinger_image)
        self.assertEqual(
            core._get_logical_screen_descriptor(self.flickinger_image, colors),
            b'\x0a\x00\x0a\x00\x91\x00\x00'
        )

    def test_get_global_color_table(self):
        colors = Counter(
            {b'\x00\x00\xff': 42, b'\xff\x00\x00': 42, b'\xff\xff\xff': 16}
        )
        color_table = core._get_global_color_table(colors)
        self.assertEqual(
            color_table,
            b'\x00\x00\xff\xff\x00\x00\xff\xff\xff\x00\x00\x00'
        )

    def test_write_gif(self):
        core.write_gif(self.flickinger_dataset, self.filename)
        with open(self.filename, 'rb') as infile:
            gif = infile.read()
        self.assertEqual(
            gif,
            b'GIF89a'
            b'\n\x00\n\x00\x91\x00\x00'
            b'\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00'
            b'!\xf9\x04\x04\x00\x00\x00\x00'
            b',\x00\x00\x00\x00\n\x00\n\x00\x00'
            b'\x02\x16\x84\x1d\x99\x87\x1a\x0c\xdc3\xa2\nu\xec'
            b'\x95\xfa\xa8\xde`\x8c\x04\x91L\x01\x00;'
        )

    def test_write_animated_gif(self):
        dataset = self.flickinger_dataset
        reversed_dataset = np.array([dataset[2], dataset[1], dataset[0]])
        core.write_gif([dataset, reversed_dataset], self.filename, fps=10)
        with open(self.filename, 'rb') as infile:
            gif = infile.read()
        self.assertEqual(
            gif,
            b'GIF89a'
            b'\n\x00\n\x00\x91\x00\x00'
            b'\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00'
            b'!\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00'
            b'!\xf9\x04\x04\n\x00\x00\x00'
            b',\x00\x00\x00\x00\n\x00\n\x00\x00'
            b'\x02\x16\x84\x1d\x99\x87\x1a\x0c\xdc3\xa2\nu\xec'
            b'\x95\xfa\xa8\xde`\x8c\x04\x91L\x01\x00'
            b'!\xf9\x04\x04\n\x00\x00\x00'
            b',\x00\x00\x00\x00\n\x00\n\x00\x00'
            b'\x02\x16\x8c\r\x99\x87\n\x1c\xdc3\xa2\nu\xec\x95'
            b'\xfa\xa8\xde`\x8c\x04\x91L\x01\x00;'
        )


if __name__ == '__main__':
    unittest.main()
