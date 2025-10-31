from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
)
from PyQt6.QtGui import QFont
import sys
from colors import Colors


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window
        self.setWindowTitle("Offline Password Manager")
        self.setGeometry(200, 200, 400, 300)  # x, y, width, height
        self.setStyleSheet(f"background-color: {Colors.DARK_GREY};")

        # set central widget (similar to panels in jpanel)
        central = QWidget()
        self.setCentralWidget(central)

        # layout for central widget
        layout = QVBoxLayout()
        central.setLayout(layout)

        # label
        label = QLabel(" - Offline Password Manager - \nlets come up with a more fun name for this :)")
        label.setFont(QFont("Segoe UI", 14))
        label.setStyleSheet(f"color: {Colors.WHITE};")
        layout.addWidget(label)

        # buttons
        generic_button = QPushButton("Generic Button")
        exit_button = QPushButton("Exit")

        # button styling
        button_style = f"""
            QPushButton {{
                background-color: {Colors.BRAT_GREEN};
                color: {Colors.WHITE};
                border-radius: 10px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BRAT_GREEN_BUTTON_HOVER};
            }}
        """
        generic_button.setStyleSheet(button_style)
        exit_button.setStyleSheet(button_style)

        # add buttons to layout
        layout.addWidget(generic_button)
        layout.addWidget(exit_button)

        # connect buttons to actions
        generic_button.clicked.connect(self.print_button_clicked)
        exit_button.clicked.connect(self.close)

    def print_button_clicked(self):
        print("button clicked")


# run
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
