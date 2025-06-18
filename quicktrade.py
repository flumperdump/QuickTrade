from PyQt6.QtWidgets import QApplication
import sys
from dashboard import MainWindow

def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    from dashboard import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
