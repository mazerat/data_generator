"""Tool to generate data files that contain statistics of abstract resource consumption per user"""

# import logging
import os
# from logging.handlers import RotatingFileHandler  # pylint: disable=C0412

import click

from utils import resource_calculator_utils
import logger


LOGGER = logger.get_logger(__name__)
# LOG_FILE = "data_generator.log"
# LOG_FOLDER = ".logs"
# LOG_FILE_SIZE_MB = 5
# LOG_FILE_BACKUP_COUNT = 5
#
TEMP_FOLDER_FOR_FILE_GENERATION = os.getenv('TEMP', '/tmp')
#
# LOG_FULL_PATH = os.path.join(LOG_FOLDER, LOG_FILE)
# os.makedirs(os.path.dirname(LOG_FULL_PATH), exist_ok=True)
#
# LOG_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# HANDLER = RotatingFileHandler(LOG_FULL_PATH,
#                               maxBytes=LOG_FILE_SIZE_MB*1024*1024,
#                               backupCount=LOG_FILE_BACKUP_COUNT)
# HANDLER.setFormatter(LOG_FORMATTER)
# HANDLER.setLevel(logging.INFO)
#
# HANDLER_STDOUT = logging.StreamHandler()
#
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.INFO)
# LOGGER.addHandler(HANDLER)
# LOGGER.addHandler(HANDLER_STDOUT)


def fill_file_by_records_count(output_folder, filename, records_amount):
    """
    Create file with provided name in a requested folder and fill it with generated content.

    :param output_folder: Folder path where new file will be created.
    :param filename: Name of a new file.
    :param records_amount: Lines amount in a new file.
    :return: None.
    """
    try:
        temporary_file_path = os.path.abspath(os.path.join(TEMP_FOLDER_FOR_FILE_GENERATION, filename))
        destination_file_path = os.path.abspath(os.path.join(output_folder, filename))
        LOGGER.info("Creating file \"%s\" and filling it with random content", temporary_file_path)
        with open(temporary_file_path, 'w') as data_file:
            for _ in range(records_amount):
                record_line = f"{str(resource_calculator_utils.generate_random_number(3))}" \
                              f" {str(resource_calculator_utils.generate_random_number(5))}\n"
                data_file.write(record_line)
        LOGGER.info("Successfully wrote file \"%s\"", temporary_file_path)

        resource_calculator_utils.move_file(temporary_file_path, destination_file_path)
    except (OSError, IOError) as exception:
        LOGGER.error("I/O error occurred during file %s processing: %s", filename, exception)
    except Exception as exception:  # pylint: disable=W0703
        LOGGER.error("Unexpected error occurred during file %s processing: %s", filename, exception)


def generate_files(output_folder, files_amount, records_amount):
    """
    Main function to trigger data files creation.

    :param output_folder: Folder path where new file will be created.
    :param files_amount: Number of files to be created in output_folder.
    :param records_amount: Lines amount in each file created.
    :return: None.
    """
    LOGGER.info("-" * 20)
    LOGGER.info("Starting file generator. Will generate %s"
                " file(s) in folder \"%s\"", files_amount, output_folder)
    resource_calculator_utils.create_data_files_directory(output_folder)

    for _ in range(files_amount):
        filename = resource_calculator_utils.generate_unique_filename_in_folder(output_folder)
        if filename:
            fill_file_by_records_count(output_folder, filename, records_amount)
        else:
            LOGGER.error("No filename was generated. Skipping this attempt.")

    LOGGER.info("Files generation completed")


@click.command()
@click.option('--output_folder', default="data_files",
              help='Output folder where generated files are stored')
@click.option('--files_amount', default=5, help='Number of files to be generated')
@click.option('--records_amount', default=10000, help='Number of records per each file')
def main(output_folder, files_amount, records_amount):
    """
    Main function for module. Accepts command line parameters.

    :param output_folder: Folder path where new file will be created.
    :param files_amount: Number of files to be created in output_folder.
    :param records_amount: Lines amount in each file created.
    :return: None.
    """
    generate_files(output_folder, files_amount, records_amount)


if __name__ == '__main__':
    main()  # pylint: disable=E1120
