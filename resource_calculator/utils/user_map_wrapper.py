# import logging
from logger import get_logger

# LOGGER = logging.getLogger(__name__)
LOGGER = get_logger(__name__)


class UserMap:
    """
    Dictionary wrapper with convenient interface for storing/updating/cleaning map of users.
    """
    def __init__(self, records_threshold=0):
        self.user_map = {}
        self.records_threshold = records_threshold

    def upsert(self, user_id, value):
        """
        Insert new key/value pair into dictionary with user_id and resource consumption value.
        Summarize values if user_id already in map.

        :param user_id: Unique user identification.
        :param value: Value of resource consumed.
        :return: None.
        """
        try:
            user_id = int(user_id)
            value = int(value)
        except ValueError as exception:
            LOGGER.error("Incorrect value provided for user_id (\"%s\")"
                         " or value (\"%s\"). The error is \"%s\"", user_id, value, exception)
            return None
        self.user_map[user_id] = self.user_map.get(user_id, 0) + value

    def __getitem__(self, item):
        return self.user_map.get(item, None)

    def __iter__(self):
        return iter(self.user_map)

    def keys(self):
        """
        Get user map keys.

        :return: dict_keys
        """
        return self.user_map.keys()

    def items(self):
        """
        Get user map items.

        :return: dict_items
        """
        return self.user_map.items()

    def values(self):
        """
        Get user map values.

        :return: dict_values
        """
        return self.user_map.values()

    def is_empty(self):
        """
        Check if user map holds no items.

        :return: bool
        """
        return len(self.user_map) == 0

    def is_full(self):
        """
        Check if user map holds items equal or more than threshold value.

        :return: bool
        """
        if self.records_threshold != 0 and len(self.keys()) >= self.records_threshold:
            return True
        return False

    def clean_map(self):
        """
        Delete everything from user map.

        :return: None
        """
        self.user_map = {}
