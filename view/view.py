import datetime
import re
import typing


class InputProcessor(typing.Protocol):
    def process_user_input(self, **kwargs: str | bool) -> None:
        ...


class View:

    def __init__(self) -> None:
        self.processor: InputProcessor | None = None

    def print_main_menu(self) -> None:
        print(
            "--------------------\n"
            "Evidence pojištěných\n"
            "--------------------\n"
            "\n"
            "Vyberte si akci:\n"
            "1 - Přidat nového pojištěného\n"
            "2 - Vypsat všechny pojištěné\n"
            "3 - Vyhledat pojištěného\n"
            "4 - Konec\n"
        )
        action = input(">> ")
        self.processor.process_user_input(menu_action=action)

    def add_insured_dialog(self) -> None:
        prompts = {
            "first_name": "Zadejte jméno pojištěného: ",
            "last_name": "Zadejte příjmení pojištěného: ",
            "date_of_birth": "Zadejte datum narození pojištěného (ve formátu 1.1.1901): ",
            "phone": "Zadejte telefonní číslo pojištěného: "
        }
        errors = {
            "first_name": "Nesprávně zadané jméno!",
            "last_name": "Nesprávně zadané příjmení!",
            "date_of_birth": "Nesprávně zadané datum narození!",
            "phone": "Nesprávně zadané telefonní číslo!"
        }
        kwargs = {}
        for pname, prompt in prompts.items():
            ok = False
            answer = ""
            while not ok:
                ok = True
                answer = input(prompt)
                if pname == "date_of_birth":
                    if not datetime.datetime.strptime("%-d.%-m.%Y", answer):
                        print(errors[pname])
                        ok = False
                elif pname == "phone":
                    if not re.match(r"^[\d\s]+$", answer):
                        ok = False
                        print(errors[pname])
            kwargs[pname] = answer
        self.processor.process_user_input(**kwargs)

    def print_insured_saved(self):
        print("Data byla uložena.")
        self.__dialog_over()

    def print_all_insured(self, data: list[dict[str, str]]):
        # header
        width = (16, 16, 4, 11)
        print("+----------------+----------------+----+-----------+")
        print("|Jméno           |Příjmení        |Věk |Telefon    |")
        print("+----------------+----------------+----+-----------+")
        for record in data:
            line = "|"
            for column, value in zip(range(4), record.values()):
                line += str(value).ljust(width[column]) + "|"
            print(line)
        print("+----------------+----------------+----+-----------+")
        self.__dialog_over()

    def search_insured_dialog(self):
        name = {
            "first_name": input("Zadejte křestní jméno: "),
            "last_name": input("Zadejte příjmení: ")
        }
        self.processor.process_user_input(**name)

    def print_operation_unsuccessful(self):
        print("Operace se nezdařila.")
        self.processor.process_user_input(dialog_over=True)

    def print_insured(self, insured):
        if not insured:
            print("Pojištěnec nenalezen.")
        else:
            width = (16, 16, 10, 11)
            line = "|"
            for column, value in zip(range(4), insured.values()):
                line += str(value).ljust(width[column]) + "|"
            print(line)
        self.__dialog_over()

    def __dialog_over(self):
        print("Pokračujte klávesou ENTER...")
        input()
        self.processor.process_user_input(dialog_over=True)
