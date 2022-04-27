import unittest

from utils.user_map_wrapper import UserMap


class TestUserMapWrapper(unittest.TestCase):

    def test_user_map_items(self):
        user_map = UserMap()
        user_map.upsert(1, 1)

        self.assertEqual(list(user_map.keys()), [1], "Error: UserMap keys are not equal to expected")
        self.assertEqual(list(user_map.items()), [(1, 1)], "Error: UserMap items are not equal to expected")
        self.assertEqual(list(user_map.values()), [1], "Error: UserMap values are not equal to expected")

        user_map.upsert(1, 1)
        self.assertEqual(list(user_map.keys()), [1], "Error: UserMap keys are not equal to expected")
        self.assertEqual(list(user_map.items()), [(1, 2)], "Error: UserMap items are not equal to expected")
        self.assertEqual(list(user_map.values()), [2], "Error: UserMap values are not equal to expected")

    def test_user_map_incorrect_items(self):
        user_map = UserMap()
        user_map.upsert("abc", 1)
        user_map.upsert(1, "abc")

        self.assertEqual(list(user_map.keys()), [], "Error: UserMap keys are not equal to expected")
        self.assertEqual(list(user_map.items()), [], "Error: UserMap items are not equal to expected")
        self.assertEqual(list(user_map.values()), [], "Error: UserMap values are not equal to expected")

    def test_user_map_is_full_is_empty(self):
        user_map = UserMap(1)
        self.assertEqual(True, user_map.is_empty(), "Error: UserMap should be empty")
        self.assertEqual(False, user_map.is_full(), "Error: UserMap should not be full")

        user_map.upsert(1, 1)

        self.assertEqual(list(user_map.keys()), [1], "Error: UserMap keys are not equal to expected")
        self.assertEqual(list(user_map.items()), [(1, 1)], "Error: UserMap items are not equal to expected")
        self.assertEqual(list(user_map.values()), [1], "Error: UserMap values are not equal to expected")
        self.assertEqual(True, user_map.is_full(), "Error: UserMap should be full")
        self.assertEqual(False, user_map.is_empty(), "Error: UserMap should not be empty")

    def test_user_map_clean(self):
        user_map = UserMap()
        user_map.upsert(1, 1)

        self.assertEqual(list(user_map.keys()), [1], "Error: UserMap keys are not equal to expected")
        self.assertEqual(list(user_map.items()), [(1, 1)], "Error: UserMap items are not equal to expected")
        self.assertEqual(list(user_map.values()), [1], "Error: UserMap values are not equal to expected")

        user_map.clean_map()
        self.assertEqual(list(user_map.keys()), [], "Error: UserMap keys are not equal to expected")
        self.assertEqual(list(user_map.items()), [], "Error: UserMap items are not equal to expected")
        self.assertEqual(list(user_map.values()), [], "Error: UserMap values are not equal to expected")

    def test_user_map_getitem(self):
        user_map = UserMap()
        user_map.upsert(1, 1)

        self.assertEqual(user_map[1], 1, "Error: UserMap keys are not equal to expected")
        self.assertIsNone(user_map[2], "Error: UserMap with non-existing key should be None")

    def test_user_map_iter(self):
        user_map = UserMap()
        user_map.upsert(1, 1)

        values = []
        for key in user_map:
            values.append(key)

        self.assertEqual(values, [1], "Error: UserMap iterator works unexpectedly")


if __name__ == "__main__":
    unittest.main()
