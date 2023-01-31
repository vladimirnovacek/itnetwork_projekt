import datetime

from interfaces import SimpleDatabase
from view import View


class Controller:
    """
    Controller controls the data flow of the app, addresses requests to necessary objects.
    """
    def __init__(self, model: SimpleDatabase, view: View) -> None:
        """
        Accepts model and view objects to communicate with.
        :param model: SimpleClientDB
        :param view: View
        """
        self.model: SimpleDatabase = model
        self.view: View = view
        self.view.processor = self
        self.running: bool = False

    def mainloop(self) -> None:
        """
        Enters an application loop.
        :return:
        """
        self.running = True
        while self.running:
            self.view.print_main_menu()

    def select_action(self, action: int) -> None:
        """
        Calls an appropriate dialog by number given as an user input.
        :param action: choice number
        :return:
        """
        match action:
            case 1:
                self.view.add_insured_dialog()
            case 2:
                data = self.model.get_all_clients()
                self.view.print_insured_table(data)
            case 3:
                self.view.search_insured_dialog()
            case 4:
                self.running = False
            case _:
                raise ValueError("Číslo musí být v rozsahu 1 - 4!")

    def add_insured(self, first_name: str, last_name: str, date_of_birth: str, phone: str) -> None:
        """
        Tries to add a new client to the database.
        :param first_name:
        :param last_name:
        :param date_of_birth:
        :param phone:
        :return:
        """
        try:
            date_of_birth = datetime.datetime.strptime(date_of_birth, "%d.%m.%Y").date()
            self.model.add_client(first_name, last_name, date_of_birth, phone)
            self.view.print_insured_saved()
        except KeyError:
            self.view.print_operation_unsuccessful()

    def search_insured(self, first_name: str, last_name: str):
        """
        Searches through the database for clients with given names and prints them.
        :param first_name:
        :param last_name:
        :return:
        """
        try:
            clients = self.model.get_clients_by_name(first_name, last_name)
        except AttributeError:
            clients = None
        self.view.print_insured_table(clients)

    def __str__(self):
        return f"Controller connected to {self.view} and {self.model}"
