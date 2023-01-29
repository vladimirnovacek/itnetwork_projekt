import datetime
import re
import typing


class InputProcessor(typing.Protocol):
    """
    Protocol class for input processing.
    """
    def process_user_input(self, **kwargs: str | bool) -> None:
        """
        Method is called by View that passes user inputs. It isn't meant to be called directly.
        :param kwargs: user inputs
        :return:
        """
        ...


class View:
    """
    Class provides user input and output and checks the validity of the input. When an InputProcessor is created,
    it has to be set as self.processor attribute value. This can be already done in its __init__() method.
    """
    def __init__(self) -> None:
        self.processor: InputProcessor | None = None

    def print_main_menu(self) -> None:
        """
        Prints main menu. User imput is passed to the input processor.
        :return:
        """
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
        try:
            action = input(">> ")
            if 1 <= int(action) <= 4:
                self.processor.process_user_input(menu_action=action)
            else:
                raise ValueError
        except (TypeError, ValueError):
            print("Neznámá volba!")
            self.__dialog_over()

    def add_insured_dialog(self) -> None:
        """
        Prints a dialog for creating a new insured. User input is passed to the input processor.
        :return:
        """
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
            kwargs[pname] = self.__get_input(pname, prompt, errors[pname])
        self.processor.process_user_input(**kwargs)

    @staticmethod
    def __get_input(pname, prompt, error):
        """
        Auxiliary method for self.add_insured_dialog method. Prints prompt, reads and validates the input and returns
        it when valid. Otherwise loops until valid input is given.
        :param pname: property that should be get
        :param prompt: text printed to user
        :param error: text printed in case of invalid input
        :return:
        """
        ok = False
        answer = ""
        while not ok:
            ok = True
            answer = input(prompt)
            if pname == "date_of_birth":
                try:
                    if datetime.datetime.strptime(answer, "%d.%m.%Y") > datetime.datetime.now():
                        raise ValueError
                except ValueError:
                    print(error)
                    ok = False
            elif pname == "phone":
                if not re.match(r"^[\d\s]+$", answer):
                    ok = False
                    print(error)
        return answer

    def print_insured_saved(self):
        """
        Prints information about successful creating a new client.
        :return:
        """
        print("Data byla uložena.")
        self.__dialog_over()

    def print_insured_table(self, data: list[dict[str, str]]) -> None:
        """
        Prints formatted list of all insured given as an argument. User input is passed to the input processor.
        :param data: list of dictionaries
        :return:
        """
        width = (32, 32, 8, 16)
        column_names = ("Jméno", "Příjmení", "Věk", "Telefon")
        line_separator = "+"
        header = "|"
        for w, c in zip(width, column_names):
            line_separator += "-" * w + "+"
            header += c.ljust(w) + "|"
        print(line_separator)
        print(header)
        print(line_separator)
        for record in data:
            line = "|"
            for column, value in zip(range(4), record.values()):
                line += str(value).ljust(width[column]) + "|"
            print(line)
        print(line_separator)
        self.__dialog_over()

    def search_insured_dialog(self) -> None:
        """
        Prints dialog for finding an insured by their name. User input is passed to the input processor.
        :return:
        """
        name = {
            "first_name": input("Zadejte křestní jméno: "),
            "last_name": input("Zadejte příjmení: ")
        }
        self.processor.process_user_input(**name)

    def print_operation_unsuccessful(self) -> None:
        """
        Prints information about unsuccessful request.
        :return:
        """
        print("Operace se nezdařila.")
        self.processor.process_user_input(dialog_over=True)

    def __dialog_over(self) -> None:
        """
        Prints an ending dialog and informs the input processor.
        :return:
        """
        print("Pokračujte klávesou ENTER...")
        input()
        self.processor.process_user_input(dialog_over=True)

    def __str__(self):
        return "View object for command line interface"
