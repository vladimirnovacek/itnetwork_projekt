from dataclasses import dataclass
import datetime


@dataclass
class Client:
    """
    Client object represents a single client providing their informations.
    """
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    phone: str

    @property
    def age(self) -> int:
        return self._get_age()

    def _get_age(self, date: datetime.date = datetime.date.today()) -> int:
        """
        If the date parameter is given, returns the age to this date, otherwise returns today's age.
        :param date: The date to which the age is being calculated.
        :return:
        """
        age = date.year - self.date_of_birth.year
        if self.date_of_birth > date.replace(year=date.year - age):
            age -= 1
        return age

    def get_client_info(self) -> dict[str, str | int]:
        """
        Gives a dictionary of name, age and phone number.
        :return: dictionary
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "phone": self.phone
        }


class SimpleClientDB:
    """
    Class used to store and manage clients.
    """
    def __init__(self, clients: list[Client] = None):
        """
        If clients attribute is given, the list of clients will be inserted into the databasse.
        :param clients: list of Client objects
        """
        if clients is None:
            clients = []
        self.clients: list[Client] = clients

    def add_client(self, first_name: str, last_name: str, date_of_birth: datetime.date, phone: str) -> None:
        """
        Creates a new client and saves them to the database.
        :param first_name:
        :param last_name:
        :param date_of_birth:
        :param phone:
        :return:
        """
        self.clients.append(Client(first_name, last_name, date_of_birth, phone))

    def get_clients_by_name(self, first_name: str, last_name: str) -> list[dict[str, str]] | None:
        """
        Searches for all clients with given name and returns them as a list.
        :param first_name:
        :param last_name:
        :return:
        """
        clients = [client.get_client_info() for client in self.clients
                   if client.first_name == first_name and client.last_name == last_name]
        return clients

    def get_all_clients(self) -> list[dict[str, str]]:
        """
        Returns list of informations of all clients in the database.
        :return:
        """
        clients = []
        for client in self.clients:
            clients.append(client.get_client_info())
        return clients

    def __str__(self):
        return f"SimpleClientDatabase holding {len(self.clients)} records"
