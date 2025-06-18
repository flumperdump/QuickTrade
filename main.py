import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from dashboard import MainWindow
from setup_wizard import SetupWizard

CONFIG_PATH = "config"
USER_PREFS_FILE = os.path.join(CONFIG_PATH, "user_prefs.json")
os.makedirs(CONFIG_PATH, exist_ok=True)

def run_main_app():
    window = MainWindow()
    window.show()
    return window

def run_setup(app):
    def on_complete():
        global main_window
        main_window = run_main_app()

    wizard = SetupWizard(on_complete)
    wizard.show()
    return wizard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    prefs_exist = os.path.exists(USER_PREFS_FILE)
    selected = []

    if prefs_exist:
        with open(USER_PREFS_FILE, 'r') as f:
            selected = json.load(f).get("selected_exchanges", [])

    if selected:
        main_window = run_main_app()
    else:
        setup_wizard = run_setup(app)

    sys.exit(app.exec())
