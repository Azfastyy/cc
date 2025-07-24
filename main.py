import sys
import requests
import psutil
import threading
import keyboard
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NM SOFTWARE")
        self.setFixedSize(300, 280)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #111111; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Croix
        close_btn = QPushButton("✕")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: red;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff8888;
            }
        """)
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(close_btn)
        layout.addLayout(top_layout)

        # Titre
        title = QLabel("NM <span style='color: #60f5ff;'>SOFTWARE</span>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Champs
        self.username = self.create_input("username", "👤")
        layout.addWidget(self.username)

        self.password = self.create_input("password", "🔒", password=True)
        layout.addWidget(self.password)

        # Bouton LAUNCH
        launch_btn = QPushButton("LAUNCH")
        launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #60f5ff;
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #42d1dd;
            }
        """)
        launch_btn.clicked.connect(self.try_login)
        layout.addSpacing(15)
        layout.addWidget(launch_btn)

        self.setLayout(layout)

    def create_input(self, placeholder, icon_text, password=False):
        wrapper = QFrame()
        wrapper.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 8px;
            }
        """)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10, 5, 10, 5)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: white;
                font-size: 14px;
            }
        """)
        if password:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)

        icon = QLabel(icon_text)
        icon.setStyleSheet("font-size: 16px; color: #888888;")

        hbox.addWidget(line_edit)
        hbox.addStretch()
        hbox.addWidget(icon)
        wrapper.setLayout(hbox)

        if password:
            self.pass_input = line_edit
        else:
            self.user_input = line_edit

        return wrapper

    def try_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        try:
            response = requests.post(
                "https://nm-api-five.vercel.app/api/check",
                json={"username": username, "password": password},
                timeout=5
            )

            try:
                data = response.json()
            except Exception:
                QMessageBox.warning(self, "Erreur", f"Erreur serveur : {response.status_code}\nRéponse invalide.")
                return

            if data.get("success") or data.get("user"):
                self.open_menu()
            else:
                QMessageBox.warning(self, "Erreur", "Identifiants invalides.")

        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Erreur", f"Connexion impossible :\n{str(e)}")

    def open_menu(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NM SOFTWARE")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #111; color: white;")
        self.init_ui()

        # Lancement de la surveillance du processus
        self.check_roblox_thread = threading.Thread(target=self.check_roblox_running, daemon=True)
        self.check_roblox_thread.start()

        # Lancement de l'écoute F5
        self.listen_f5_thread = threading.Thread(target=self.listen_f5_key, daemon=True)
        self.listen_f5_thread.start()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        close_btn = QPushButton("✕")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: red;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff8888;
            }
        """)
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)

        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_btn)
        layout.addLayout(close_layout)

        label = QLabel("Roblox Cheat")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: #60f5ff;")
        layout.addWidget(label)

        layout.addSpacing(20)

        load_btn = QPushButton("LOAD")
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #60f5ff;
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #42d1dd;
            }
        """)
        load_btn.clicked.connect(self.show_please_open)
        layout.addWidget(load_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.msg = QLabel("")
        self.msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg.setStyleSheet("font-size: 14px; color: #aaaaaa;")
        layout.addSpacing(10)
        layout.addWidget(self.msg)

        self.setLayout(layout)

    def show_please_open(self):
        self.msg.setText("Please open the game")

    def check_roblox_running(self):
        while True:
            if any(proc.name().lower() == "robloxplayerbeta.exe" for proc in psutil.process_iter()):
                self.close()
                break

    def listen_f5_key(self):
        keyboard.wait("F5")
        self.show_cheat_menu()

    def show_cheat_menu(self):
        # Tu peux ouvrir un menu custom ici
        QMessageBox.information(self, "Cheat Menu", "Cheat menu ouvert (simulation).")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
