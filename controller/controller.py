
from view.view import View
from model.simple_client_database import SimpleClientDB


class Controller:
    def __init__(self, model: SimpleClientDB, view: View):
        self.model: SimpleClientDB = model
        self.view: View = view
        self.view.processor = self
        self.running: bool = False
        self.__option_selected = 0

    def mainloop(self) -> None:
        self.running = True
        while self.running:
            self.view.print_main_menu()

    def process_user_input(self, **kwargs: str | bool) -> None:
        if "menu_action" in kwargs:
            self.call_dialog(int(kwargs["menu_action"]))
        elif "dialog_over" in kwargs:
            return
        elif self.__option_selected == 1:
            try:
                self.model.add_client(**kwargs)
                self.view.print_insured_saved()
            except KeyError:
                self.view.print_operation_unsuccessful()
        elif self.__option_selected == 2:
            data = self.model.get_all_clients()
            self.view.print_all_insured(data)
        elif self.__option_selected == 3:
            try:
                client = self.model.get_client_by_name(**kwargs).get_client_info()
            except AttributeError:
                client = None
            self.view.print_insured(client)

    def call_dialog(self, number: int) -> None:
        self.__option_selected = number
        match number:
            case 1:
                self.view.add_insured_dialog()
            case 2:
                data = self.model.get_all_clients()
                self.view.print_all_insured(data)
            case 3:
                self.view.search_insured_dialog()
            case 4:
                self.running = False
            case _:
                raise ValueError("Číslo musí být v rozsahu 1 - 4!")
