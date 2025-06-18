from quicktrade import launch_app

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    from dashboard import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

