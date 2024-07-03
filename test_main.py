import unittest

from main import FakeDu
from pathlib import Path

import os


class TestFakeDu(unittest.TestCase):

    def test_search_depth_1(self):
        root_path = os.path.join(os.getcwd(), "resources")
        files = FakeDu.search(Path(root_path), '*', 1)
        self.assertEqual(len(files), 2)

    def test_search_depth_0(self):
        root_path = os.path.join(os.getcwd(), "resources")
        files = FakeDu.search(Path(root_path), '*', 0)
        self.assertTrue(len(files), 4)

    def test_format_bytes(self):
        testFile = Path(os.getcwd(), "resources/test.txt")
        res = FakeDu.format_size(FakeDu.file_size(testFile), "B")
        self.assertEqual(res, "18B")

    def test_format_mbytes(self):
        testFile = Path(os.getcwd(), "resources/test.txt")
        res = FakeDu.format_size(FakeDu.file_size(testFile), "MB")
        self.assertEqual(res, "0.00001716613769531250MB")

    def test_format_mbytes(self):
        testFile = Path(os.getcwd(), "resources/test.txt")
        res = FakeDu.format_size(FakeDu.file_size(testFile), "GB")
        self.assertEqual(res, "0.00000001676380634308GB")

    def test_search_empty_array(self):
        res = FakeDu.search(Path(os.path.join(os.getcwd(), "fakedu/resources/test5")), "*", 0)
        self.assertEqual(len(res), 0)

    def test_search_empty_array(self):
        res = FakeDu.search(Path(os.path.join(os.getcwd(), "fakedu/resources/test5")), "*", 0)
        self.assertEqual(len(res), 0)

    def test_search_match_py(self):
        root_path = os.path.join(os.getcwd(), "resources")
        files = FakeDu.search(Path(root_path), '*.py', 0)
        self.assertTrue(len(files), 1)


if __name__ == '__main__':
    unittest.main()