import unittest
import os
import uuid
import shutil
import re

from utils import resource_calculator_utils


class TestResourceCalculatorUtils(unittest.TestCase):
    temp_folder = os.getenv('TEMP', '/tmp')

    def test_numbers_amount_1(self):
        generated_number = resource_calculator_utils.generate_random_number(1)
        self.assertTrue(1 <= generated_number < 10,
                        f"Error: generated number {generated_number} does not fit to interval 1 <= X < 10")

    def test_numbers_amount_2(self):
        generated_number = resource_calculator_utils.generate_random_number(2)
        self.assertTrue(10 <= generated_number < 100,
                        f"Error: generated number {generated_number} does not fit to interval 10 <= X < 100")

    def test_numbers_amount_3(self):
        generated_number = resource_calculator_utils.generate_random_number(3)
        self.assertTrue(100 <= generated_number < 1000,
                        f"Error: generated number {generated_number} does not fit to interval 100 <= X < 1000")

    def test_numbers_amount_4(self):
        generated_number = resource_calculator_utils.generate_random_number(4)
        self.assertTrue(1000 <= generated_number < 10000,
                        f"Error: generated number {generated_number} does not fit to interval 1000 <= X < 10000")

    def test_numbers_amount_0(self):
        generated_number = resource_calculator_utils.generate_random_number(0)
        self.assertEqual(0, generated_number,
                         f"Error: generated number {generated_number} is not equal to 0")

    def test_numbers_amount_negative(self):
        generated_number = resource_calculator_utils.generate_random_number(-1)
        self.assertEqual(0, generated_number,
                         f"Error: generated number {generated_number} is not equal to 0")

    def test_unique_filename_generation(self):
        filename = resource_calculator_utils.generate_unique_filename_in_folder(".")
        self.assertTrue(filename.startswith("data_file_"))
        self.assertTrue(filename.endswith(".txt"))
        self.assertTrue(len(re.findall("(data_file_)[a-zA-Z0-9]*(.txt)", filename)) != 0,
                        f"Error: filename does not follow re pattern")

    def test_create_data_files_directory(self):
        folder_name = uuid.uuid4().hex
        full_path = os.path.join(self.temp_folder, folder_name)

        resource_calculator_utils.create_data_files_directory(full_path)
        resource_calculator_utils.create_data_files_directory(full_path)
        dir_exists = os.path.isdir(full_path)
        shutil.rmtree(full_path, ignore_errors=True)

        self.assertTrue(dir_exists, f"Error: created directory can not be found")

    def test_move_file(self):
        initial_test_file_path = os.path.join(self.temp_folder, uuid.uuid4().hex)
        open(initial_test_file_path, 'a').close()
        destination_test_file_path = os.path.join(self.temp_folder, uuid.uuid4().hex)
        resource_calculator_utils.move_file(initial_test_file_path, destination_test_file_path)
        file_exists = os.path.isfile(destination_test_file_path)
        os.remove(destination_test_file_path)

        self.assertTrue(file_exists, f"Error: moved file can not be found")

    def test_get_first_file_in_folder(self):
        test_folder = os.path.join(self.temp_folder, uuid.uuid4().hex)
        os.mkdir(test_folder)

        test_file_path_1 = os.path.join(test_folder, "1.txt")
        test_file_path_2 = os.path.join(test_folder, "2.txt")
        open(test_file_path_1, 'w').close()
        open(test_file_path_2, "w").close()
        first_file = resource_calculator_utils.get_first_file_in_folder(test_folder)
        shutil.rmtree(test_folder)

        self.assertEqual(test_file_path_1, first_file, "Error: expected another filename")


if __name__ == "__main__":
    unittest.main()
