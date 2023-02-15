
import sqlite3
import typing


class Address(typing.TypedDict):
    country: str
    city: str
    street: str
    house_number: int | None
    building_id_no: int
    postal_code: str


class Contacts(typing.TypedDict):
    phone: str
    email: str


class UserInfo(typing.TypedDict):
    first_name: str
    last_name: str
    pid_number: int
    domicile: Address
    mailing_address: Address
    contacts: Contacts


class SQLiteDatabaseHandler:

    def __init__(self, filename: str):
        self.sqlite_connection = sqlite3.connect(filename)
        self.cursor = self.sqlite_connection.cursor()

    def insert_user(self, user_info: UserInfo):
        domicile = self._insert_address(user_info["domicile"])
        mailing_address = self._insert_address(user_info["mailing_address"])
        user_info = dict(user_info)
        user_info["domicile"] = domicile
        user_info["mailing_address"] = mailing_address
        user_id = self.cursor.execute("""
            SELECT id_user FROM users
            WHERE pid_number = :pid_number
        """, user_info).fetchone()[0]
        if not user_id:
            pass
        self.sqlite_connection.commit()

    def _insert_address(self, address: Address) -> int:
        def get_address_id():
            return self.cursor.execute("""
                SELECT id_address FROM addresses
                WHERE country = :country
                    AND city = :city
                    AND street = :street
                    AND building_id_no = :building_id_no
                    AND postal_code = :postal_code;
            """, address).fetchone()[0]
        address_id = get_address_id()
        if not address_id:
            self.cursor.execute("""
                INSERT INTO addresses (
                    country, city, street, house_number, building_id_no, postal_code
                ) VALUES (
                    :country, :city, :street, :house_number, :building_id_no, :postal_code
                );
            """, address)
            address_id = get_address_id()
        return address_id


if __name__ == '__main__':
    db = SQLiteDatabaseHandler("insurance_company.db")
    user = {
        "first_name": "Vladimír",
        "last_name": "Nováček",
        "domicile": {
            "country": "Česká republika",
            "city": "Lázně Toušeň",
            "street": "Za Školou",
            "house_number": 11,
            "building_id_no": 12,
            "postal_code": "25089"
        },
        "mailing_address": {
            "country": "Česká republika",
            "city": "Lázně Toušeň",
            "street": "Písecká",
            "house_number": None,
            "building_id_no": 2,
            "postal_code": "25089"
        },
        "contacts": {
            "phone": "728 563 374",
            "email": "novacek.vladimir@gmail.com"
        }
    }
    db.insert_user(user)
