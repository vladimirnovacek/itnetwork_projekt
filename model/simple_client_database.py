import dataclasses
import datetime


@dataclasses.dataclass
class Client:
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    phone: str

    def get_age(self, date: datetime.date = datetime.date.today()) -> int:
        age = date.year - self.date_of_birth.year
        if self.date_of_birth > date.replace(year=date.year - age):
            age -= 1
        return age

    def get_client_info(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.get_age(),
            "phone": self.phone
        }


class SimpleClientDB:
    def __init__(self, clients: list[Client] = None):
        if clients is None:
            clients = []
        self.clients: list[Client] = clients

    def add_client(self, first_name: str, last_name: str, date_of_birth: str, phone: str) -> None:
        date_of_birth = datetime.datetime.strptime(date_of_birth, "%d.%m.%Y").date()
        self.clients.append(Client(first_name, last_name, date_of_birth, phone))

    def get_client_by_name(self, first_name: str, last_name: str) -> Client | None:
        for client in self.clients:
            if client.first_name == first_name and client.last_name == last_name:
                return client
        return None

    def get_all_clients(self) -> list[dict[str, str]]:
        clients = []
        for client in self.clients:
            clients.append(client.get_client_info())
        return clients
