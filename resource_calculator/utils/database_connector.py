import sqlite3
import sys
# import logging
from logger import get_logger

from .user_map_wrapper import UserMap


# LOGGER = logging.getLogger(__name__)
LOGGER = get_logger(__name__)


class DatabaseConnector:
    """
    Wrapper for database connection with convenient interface for
    managing connection and query database.
    """
    def __init__(self, database_file):
        self.connection = None
        self.database_file = database_file
        self.create_connection()
        self.table_name = "user_resource_consumption"

    def create_connection(self):
        """
        Create database connection to the SQLite database
        specified by the database_file.

        :return: None
        """
        try:
            self.connection = sqlite3.connect(self.database_file)
            LOGGER.info("Database connection created successfully")
        except sqlite3.Error as exception:
            LOGGER.error("Error establishing connection to database: %s", exception)
            sys.exit(1)

    def create_database(self):
        """
        Create new table to be filled.

        :return: None
        """
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS %s (
                                    id INTEGER NOT NULL PRIMARY KEY,
                                    resource INTEGER NOT NULL
                                    );''' % self.table_name
        self.execute_statement(sqlite_create_table_query)

    def execute_statement(self, request):
        """
        Execute request and return output from database.

        :param request: SQL request to be executed.
        :return: SQL request output
        """
        if self.connection is not None:
            cursor = None
            try:
                cursor = self.connection.cursor()
                result = cursor.execute(request).fetchall()
                self.connection.commit()
                return result
            except sqlite3.Error as exception:
                LOGGER.error("Error during request execution in database: %s\nRequest: %s", exception, request)

                sys.exit(1)
            finally:
                if cursor is not None:
                    cursor.close()
        else:
            LOGGER.error("Database connection is not established")
            return None

    def upsert_users(self, user_map: UserMap):
        """
        Insert new users and update existing ones based on values accumulated in user_map.

        :param user_map: Map of users and resource consumption.
        :return: SQL request output
        """
        request = '''
INSERT INTO %s
    (id, resource)
VALUES
%s
ON CONFLICT(id) DO UPDATE SET resource=resource + excluded.resource;
        ''' % (self.table_name,
               ",\n".join(["\t(%s, %s)" % (k, v) for k, v in list(user_map.items())]))
        return self.execute_statement(request)

    def __del__(self):
        if self.connection is not None:
            self.connection.close()
        LOGGER.info("Connection closed")
