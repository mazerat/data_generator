import uuid
from random import randint
import os
import sys
import shutil

from logger import get_logger

LOGGER = get_logger(__name__)


def generate_random_number(digits_amount: int) -> int:
    """
    Generate random number of digits_amount numbers length. E.g., if digits_amount = 3,
    generated number will belong to interval between 100 and 999.

    :param digits_amount: number of digits in the returned number.
    :return: Generated number for all positive integers, 0 if digits_amount <= 0.
    """
    if digits_amount > 0:
        range_start = 10 ** (digits_amount - 1)
        range_end = (10 ** digits_amount) - 1
        return randint(range_start, range_end)
    return 0


def generate_unique_filename_in_folder(folder, max_tries=10):
    """
    Generate unique filename and make sure it does not exist in particular folder.

    :param folder: Path to a folder where file with generated name is supposed to be stored.
    :param max_tries: Loop retry maximum count to try to generate unique filename.
    :return: New unique filename.
    """
    def generate_filename():
        """
        Generate random file name.

        :return: New unique filename.
        """
        new_filename = f"data_file_{str(uuid.uuid4().hex)}.txt"
        LOGGER.debug("Generated new file name \"%s\"", new_filename)
        return new_filename

    filename = generate_filename()

    tries_count = 1
    while os.path.exists(os.path.join(folder, filename)):
        LOGGER.debug("File \"%s\" exist in folder \"%s\"", filename, folder)
        filename = generate_filename()
        if tries_count > max_tries:
            LOGGER.error("Failed to generate unique file name after %s retries", max_tries)
            return None
        tries_count += 1
    return filename


def create_data_files_directory(path):
    """
    Create folder by the provided path or make sure it exists already.

    :param path: Absolute or relational path of a folder to be created.
    :return: None
    """
    abs_path = os.path.abspath(path)
    LOGGER.debug("Will create \"%s\" folder or make sure it exists already", abs_path)
    try:
        os.makedirs(abs_path, exist_ok=True)
        LOGGER.debug("Directory \"%s\" exist", abs_path)
    except Exception as exception:  # pylint: disable=W0703
        LOGGER.error("Failed to create output directory \"%s\""
                     " with the following error: \"%s\"", abs_path, exception)
        sys.exit(1)


def move_file(temporary_file_path, destination_file_path):
    """
    Replace file from temporary file path to destination_file_path.

    :param temporary_file_path: Current file location.
    :param destination_file_path: Desired file location.
    :return: None.
    """
    LOGGER.info("Moving temporary file %s to permanent location %s",
                temporary_file_path, destination_file_path)
    shutil.move(temporary_file_path, destination_file_path)
    LOGGER.info("Successfully moved file \"%s\"", destination_file_path)


def get_first_file_in_folder(data_files_folder):
    """
    Get first file name in a provided folder.

    :param data_files_folder: Folder to be examined.
    :return: Filename or None.
    """
    return next(
        (
            os.path.join(data_files_folder, f) for f in os.listdir(data_files_folder)
            if os.path.isfile(os.path.join(data_files_folder, f))
        ),
        None)
