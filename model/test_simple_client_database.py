import datetime

import simple_client_database
import unittest


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_age(self) -> None:
        client = simple_client_database.Client("John", "Brown", datetime.date(1985, 11, 7), "123456789")
        self.assertEqual(37, client.get_age(datetime.date(2023, 1, 29)))
        client = simple_client_database.Client("John", "Brown", datetime.date(1985, 1, 7), "123456789")
        self.assertEqual(38, client.get_age(datetime.date(2023, 1, 29)))
        client = simple_client_database.Client("John", "Brown", datetime.date(1985, 1, 29), "123456789")
        self.assertEqual(38, client.get_age(datetime.date(2023, 1, 29)))

    def test__str__(self):
        client = simple_client_database.Client("John", "Brown", datetime.date(1985, 11, 7), "123456789")
        print(repr(client))
