
import view
import unittest


class DummyProcessor:
    def __init__(self):
        self.kwargs = {}

    def process_user_input(self, **kwargs):
        self.kwargs = kwargs
        print(kwargs)


class TestClient(unittest.TestCase):

    viewInstance: view.View

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.processor = DummyProcessor()
        self.viewInstance = view.View(self.processor)

    def tearDown(self) -> None:
        pass

    def test_main_menu(self):
        self.viewInstance.print_main_menu()
        self.assertIn("menu_action", self.processor.kwargs)

    def test_add_insured_dialog(self):
        self.viewInstance.add_insured_dialog()

    def test_print_all_insured(self):
        data = [
            {"first_name": "Adam", "last_name": "Anděl", "date_of_birth": "1.1.1911", "phone": "111 111 111"},
            {"first_name": "Bedřich", "last_name": "Bílý", "date_of_birth": "22.2.1922", "phone": "222 222 222"},
            {"first_name": "Cyril", "last_name": "Cibulka", "date_of_birth": "3.10.1933", "phone": "333333333"},
            {"first_name": "David", "last_name": "Doškář", "date_of_birth": "14.12.1944", "phone": "44 4444 444"}
        ]
        self.viewInstance.print_all_insured(data)
