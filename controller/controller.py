import datetime

from view.view import View
from model.simple_client_database import SimpleClientDB


class Controller:
    """
    Controller controls the data flow of the app, addresses requests to necessary objects.
    """
    def __init__(self, model: SimpleClientDB, view: View) -> None:
        """
        Accepts model and view objects to communicate with.
        :param model: SimpleClientDB
        :param view: View
        """
        self.model: SimpleClientDB = model
        self.view: View = view
        self.view.processor = self
        self.running: bool = False
        self.__option_selected: int = 0

    def mainloop(self) -> None:
        """
        Enters an application loop.
        :return:
        """
        self.running = True
        while self.running:
            self.view.print_main_menu()

    def process_user_input(self, **kwargs: str | bool) -> None:
        """
        Method is called by View that passes user inputs. It isn't meant to be called directly.
        :param kwargs: user inputs
        :return:
        """
        if "menu_action" in kwargs:
            self.__call_dialog(int(kwargs["menu_action"]))
        elif "dialog_over" in kwargs:
            return
        elif self.__option_selected == 1:
            try:
                kwargs = dict(kwargs)  # this is done to avoid "Incorrect type" warning in the next line
                kwargs["date_of_birth"] = datetime.datetime.strptime(kwargs["date_of_birth"], "%d.%m.%Y").date()
                self.model.add_client(**kwargs)
                self.view.print_insured_saved()
            except KeyError:
                self.view.print_operation_unsuccessful()
        elif self.__option_selected == 2:
            data = self.model.get_all_clients()
            self.view.print_insured_table(data)
        elif self.__option_selected == 3:
            try:
                clients = self.model.get_clients_by_name(**kwargs)
            except AttributeError:
                clients = None
            self.view.print_insured_table(clients)

    def __call_dialog(self, number: int) -> None:
        """
        Calls an appropriate dialog by number given as an user input.
        :param number: choice number
        :return:
        """
        self.__option_selected = number
        match number:
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

    def __str__(self):
        return f"Controller connected to {self.view} and {self.model}"
