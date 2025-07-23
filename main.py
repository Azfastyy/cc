import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QObject
import psutil  # pip install psutil

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.user_label = QLabel("Username:")
        self.user_input = QLineEdit()

        self.pass_label = QLabel("Password:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.try_login)

        self.layout.addWidget(self.user_label)
        self.layout.addWidget(self.user_input)
        self.layout.addWidget(self.pass_label)
        self.layout.addWidget(self.pass_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def try_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        try:
            response = requests.post(
                "https://nm-api.vercel.app/check",
                json={"username": username, "password": password},
                timeout=5
            )
            data = response.json()
            if data.get("success"):
                self.open_menu()
            else:
                QMessageBox.warning(self, "Erreur", "Identifiants invalides.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Problème de connexion:\n{e}")

    def open_menu(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roblox Cheat")
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Roblox cheat")
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_clicked)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)

    def load_clicked(self):
        self.label.setText("Please start your game")
        # Démarre un timer pour vérifier si le jeu est lancé
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_game)
        self.timer.start(2000)  # toutes les 2 secondes

    def check_game(self):
        # Ex: détecter si un processus "RobloxPlayer.exe" tourne
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == "RobloxPlayer.exe":
                self.timer.stop()
                self.close()
                break


class AppController(QObject):  # Hérite de QObject pour installEventFilter
    def __init__(self):
        super().__init__()  # Initialise QObject
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow()
        self.login_window.show()

        # Raccourci F5 pour rouvrir la fenêtre menu
        self.app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_F5:
                # Ouvre la fenêtre menu si pas déjà ouverte
                if not hasattr(self, 'menu_window') or not self.menu_window.isVisible():
                    self.menu_window = MenuWindow()
                    self.menu_window.show()
                return True
        return False

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
