from PyQt6.QtWidgets import QApplication
import sys
from dashboard import MainWindow

def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
