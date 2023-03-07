import unittest
from pathlib import Path
import shutil
from zipfile import ZipFile
from functools import reduce
from itertools import combinations

from generate_archives import (
    generate_archives, num_zips, num_xmls_in_zip, max_objects_in_xml
)
from make_reports import make_reports


class TestArchives(unittest.TestCase):
    def setUp(self):
        self.archives_path = Path('archives')
        self.reports_path = Path('reports')
        self.clean_directory(self.archives_path)
        self.clean_directory(self.reports_path)

    def clean_directory(self, directory):
        path = Path(directory)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir()

    def test_archives_number(self):
        generate_archives()
        self.assertEqual(len(list(self.archives_path.iterdir())), num_zips)

    def test_xmls_number(self):
        def sum_zip_files(len1, zip_path):
            with ZipFile(zip_path, 'r') as zip_file:
                return len1 + len(zip_file.namelist())

        generate_archives()
        expected = int(num_zips * num_xmls_in_zip)
        actual = reduce(sum_zip_files, self.archives_path.iterdir(), 0)
        self.assertEqual(actual, expected)

    def test_objects_number(self):
        generate_archives()
        make_reports()
        expected_min = num_zips * num_xmls_in_zip
        expected_max = num_zips * num_xmls_in_zip * max_objects_in_xml
        with open(self.reports_path / 'objects.csv', 'r') as objects:
            actual = len(objects.readlines())
        self.assertGreaterEqual(actual, expected_min)
        self.assertLessEqual(actual, expected_max)

    def test_id_uniqueness(self):
        generate_archives()
        make_reports()
        with open(self.reports_path / 'levels.csv', 'r') as levels_file:
            levels = levels_file.readlines()
        ids = [i.split(',')[0] for i in levels]
        self.assertEqual(len(ids), num_zips * num_xmls_in_zip)
        for left, right in combinations(ids, 2):
            self.assertNotEqual(left, right)

    def tearDown(self) -> None:
        shutil.rmtree(self.archives_path)
        shutil.rmtree(self.reports_path)


if __name__ == '__main__':
    unittest.main()
