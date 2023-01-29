import datetime

from controller.controller import Controller
from model.simple_client_database import SimpleClientDB, Client
from view.view import View


def main():
    sample = [
        Client("Vláďa", "Nováček", datetime.date(2015, 1, 8), "000 000 000"),
        Client("Jana", "Nováčková", datetime.date(1986, 8, 19), "775 971 895"),
        Client("Vladimír", "Nováček", datetime.date(1985, 11, 7), "728 563 374")
    ]
    model = SimpleClientDB(sample)
    view = View()
    controller = Controller(model, view)
    controller.mainloop()


if __name__ == '__main__':
    main()
