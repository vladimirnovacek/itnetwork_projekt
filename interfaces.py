import datetime
from typing import Protocol


class SimpleDatabase(Protocol):
    """
    Protocol class offering the interface to a database.
    """

    def add_client(self, first_name: str, last_name: str, date_of_birth: datetime.date, phone: str) -> None:
        """
        Creates a new client and saves them to the database.
        :param first_name:
        :param last_name:
        :param date_of_birth:
        :param phone:
        :return:
        """
        ...

    def get_clients_by_name(self, first_name: str, last_name: str) -> list[dict[str, str]] | None:
        """
        Searches for all clients with given name and returns them as a list.
        :param first_name:
        :param last_name:
        :return:
        """
        ...

    def get_all_clients(self) -> list[dict[str, str]]:
        """
        Returns list of informations of all clients in the database.
        :return:
        """
        ...


class InputProcessor(Protocol):
    """
    Protocol class that offers an interface for processing the input in the application.
    """

    def select_action(self, action: int) -> None:
        """
        Calls an appropriate dialog by number given as an user input.
        :param action: choice number
        :return:
        """
        ...

    def add_insured(self, first_name: str, last_name: str, date_of_birth: str, phone: str) -> None:
        """
        Tries to add a new client to the database
        :param first_name:
        :param last_name:
        :param date_of_birth:
        :param phone:
        :return:
        """
        ...

    def search_insured(self, first_name: str, last_name: str) -> None:
        """
        Searches through the database for clients with given names and prints them.
        :param first_name:
        :param last_name:
        :return:
        """
        ...
