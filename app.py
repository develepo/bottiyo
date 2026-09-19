import sys

from PySide6.QtWidgets import QApplication

from desk.pet import PetWindow


def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Bottiyo"
    )

    pet = PetWindow()

    pet.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()