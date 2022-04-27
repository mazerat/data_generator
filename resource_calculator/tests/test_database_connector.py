import os
import unittest
import uuid

from utils.database_connector import DatabaseConnector
from utils.user_map_wrapper import UserMap


class TestDatabaseConnector(unittest.TestCase):
    temp_folder = os.getenv('TEMP', '/tmp')

    def test_database_connector_empty_tables(self):
        database_file = os.path.join(self.temp_folder, f"{uuid.uuid4().hex}.db")
        database_connection = DatabaseConnector(database_file)
        response = database_connection.execute_statement(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{database_connection.table_name}';")

        del database_connection
        os.remove(database_file)

        self.assertEqual(response, [], "Error: newly created database holds tables")

    def test_database_connector_create_table(self):
        database_file = os.path.join(self.temp_folder, f"{uuid.uuid4().hex}.db")
        database_connection = DatabaseConnector(database_file)
        database_connection.create_database()

        table_name = database_connection.table_name
        response = database_connection.execute_statement(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{database_connection.table_name}';")

        del database_connection
        os.remove(database_file)

        self.assertEqual([(table_name, )], response, "Error: list of created database is not equal to expected")

    def test_database_connector_upsert_users(self):
        database_file = os.path.join(self.temp_folder, f"{uuid.uuid4().hex}.db")
        database_connection = DatabaseConnector(database_file)
        database_connection.create_database()

        user_map = UserMap()
        user_map.upsert(1, 1)

        database_connection.upsert_users(user_map)

        response = database_connection.execute_statement(
            f"SELECT * FROM {database_connection.table_name};")

        del database_connection
        os.remove(database_file)

        self.assertEqual([(1, 1)], response, "Error: list of provisioned users is not equal to expected")


if __name__ == "__main__":
    unittest.main()
