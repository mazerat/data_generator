import os
import shutil
import unittest
import uuid

from data_generator import fill_file_by_records_count, generate_files


class TestDataGenerator(unittest.TestCase):
    temp_folder = os.getenv('TEMP', '/tmp')

    def test_fill_file_by_records_count(self):
        test_filename = uuid.uuid4().hex
        fill_file_by_records_count(self.temp_folder, test_filename, 1)

        with open(os.path.join(self.temp_folder, test_filename)) as test_file:
            data = test_file.readlines()

        self.assertEqual(1, len(data), f"Error: file contains {len(data)} records, but should have contained 1")

    def test_generate_files(self):
        test_folder = os.path.join(self.temp_folder, uuid.uuid4().hex)
        generate_files(test_folder, 2, 1)
        files = os.listdir(test_folder)
        shutil.rmtree(test_folder)

        self.assertEqual(2, len(files), "Error: test folder contains not expected amount of files")


if __name__ == "__main__":
    unittest.main()
