import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NM SOFTWARE")
        self.setFixedSize(300, 280)
        self.setStyleSheet("background-color: #111111; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("NM <span style='color: #60f5ff;'>SOFTWARE</span>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Username field with icon
        self.username = self.create_input("username", "👤")
        layout.addWidget(self.username)

        # Password field with icon
        self.password = self.create_input("password", "🔒", password=True)
        layout.addWidget(self.password)

        # Launch button
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

        # Sauvegarde pour accès direct
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
                "https://nm-api.vercel.app/api/check",
                json={"username": username, "password": password},
                timeout=5
            )
            data = response.json()
            if data.get("success") or data.get("user"):
                self.open_menu()
            else:
                QMessageBox.warning(self, "Erreur", "Identifiants invalides.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Connexion impossible:\n{e}")

    def open_menu(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roblox Cheat")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #111; color: white;")
        layout = QVBoxLayout()
        label = QLabel("Logged in.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
