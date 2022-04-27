"""Tool to parse data files and upload statistics of abstract resource consumption per user"""

import os
import time

import click

import logger
from utils import (database_connector, resource_calculator_utils,
                   user_map_wrapper)


LOGGER = logger.get_logger(__name__)


def upload_data_to_db_by_chunks(db_connector, user_map, file):
    """
    Split data from files by chunks and after that upload everything to database.

    :param db_connector: Object of class-wrapper for Database connection.
    :param user_map: Map that is filled with data from files.
    :param file: Path to SQL database file.
    :return: None
    """
    try:
        with open(file, 'r') as data_file:
            for line in data_file:
                user, resource = line.split()
                if user_map.is_full():
                    db_connector.upsert_users(user_map)
                    user_map.clean_map()
                user_map.upsert(user, resource)
    except (OSError, IOError) as exception:
        LOGGER.error("Error during data provisioning: %s", exception)


def parse_files(data_files_folder, backup_directory, database_file, map_max_size):
    """
    Main function to trigger data files parsing.

    :param data_files_folder: Folder where data files are stored.
    :param backup_directory: Folder where parsed files are moved.
    :param database_file: Full path to database file (SQLite) where all records will be stored.
    :param map_max_size: Maximum map size before dumping to database.
    :return: None
    """
    resource_calculator_utils.create_data_files_directory(backup_directory)

    user_map = user_map_wrapper.UserMap(map_max_size)

    db_connector = database_connector.DatabaseConnector(database_file)
    db_connector.create_database()

    try:
        while True:
            next_file = resource_calculator_utils.get_first_file_in_folder(data_files_folder)
            if next_file is not None:
                upload_data_to_db_by_chunks(db_connector, user_map, next_file)
                resource_calculator_utils.move_file(next_file,
                                                    os.path.join(backup_directory, os.path.basename(next_file)))
            else:
                if not user_map.is_empty():
                    db_connector.upsert_users(user_map)
                time.sleep(5)
    except KeyboardInterrupt:
        if not user_map.is_empty():
            db_connector.upsert_users(user_map)

    LOGGER.info("Finished")


@click.command()
@click.option('--data_files_folder', default="data_files",
              help='Folder where data files are stored')
@click.option('--backup_directory', default="backup",
              help='Folder where processed files are backed up')
@click.option('--database_file', default="db_file.db",
              help='SQLite database file path')
@click.option('--map_max_size', default=10,
              help='Max amount of key-value pairs accumulated before dumping to database')
def main(data_files_folder, backup_directory, database_file, map_max_size):
    """
    Main function for module. Accepts command line parameters.

    :param data_files_folder: Folder path where data files are stored.
    :param backup_directory: Folder to place parsed files for backup.
    :param database_file: Full path to SQLLite database file.
    :param map_max_size: Max amount of key-value pairs accumulated before dumping to database
    :return: None.
    """
    parse_files(data_files_folder, backup_directory, database_file, map_max_size)


if __name__ == "__main__":
    main()  # pylint: disable=E1120
