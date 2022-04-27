import os
import unittest
import uuid

from data_parser import upload_data_to_db_by_chunks
from utils.database_connector import DatabaseConnector
from utils.user_map_wrapper import UserMap


class TestDataParser(unittest.TestCase):
    temp_folder = os.getenv('TEMP', '/tmp')

    def test_upload_data_to_db_by_chunks(self):
        database_file = os.path.join(self.temp_folder, f"{uuid.uuid4().hex}.db")
        database_connection = DatabaseConnector(database_file)
        database_connection.create_database()

        user_map = UserMap(1)
        user_map.upsert(1, 1)

        data_file_path = os.path.join(self.temp_folder, uuid.uuid4().hex)
        with open(data_file_path, "w") as data_file:
            data_file.write("1 1")

        upload_data_to_db_by_chunks(database_connection, user_map, data_file_path)

        response = database_connection.execute_statement(
            f"SELECT * FROM {database_connection.table_name};")

        del database_connection
        os.remove(database_file)
        os.remove(data_file_path)

        self.assertEqual([(1, 1)], response, "Error: list of provisioned users is not equal to expected")


if __name__ == "__main__":
    unittest.main()
