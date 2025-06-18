from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QScrollArea,
    QHBoxLayout, QLineEdit, QMessageBox
)
import os
import json

CONFIG_PATH = "config"
USER_PREFS_FILE = os.path.join(CONFIG_PATH, "user_prefs.json")
API_KEYS_FILE = os.path.join(CONFIG_PATH, "api_keys.json")

EXCHANGES = ["Bybit", "Kraken", "Binance", "KuCoin", "Coinbase", "MEXC", "Bitget", "Crypto.com", "Hyperliquid"]

os.makedirs(CONFIG_PATH, exist_ok=True)

class SetupWizard(QWidget):
    def __init__(self, on_complete_callback):
        super().__init__()
        self.setWindowTitle("QuickTrade Setup Wizard")
        self.setMinimumWidth(500)
        self.on_complete = on_complete_callback
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel("✅ Welcome to QuickTrade Setup!\n\nSelect the exchanges you use:"))

        self.checkboxes = {}
        for name in EXCHANGES:
            cb = QCheckBox(name)
            cb.setChecked(False)
            self.checkboxes[name] = cb
            self.layout().addWidget(cb)

        self.api_inputs = {}
        self.layout().addWidget(QLabel("\n🔐 Enter your API keys:"))
        for name in EXCHANGES:
            row = QHBoxLayout()
            key_input = QLineEdit()
            key_input.setPlaceholderText("API Key")
            secret_input = QLineEdit()
            secret_input.setPlaceholderText("API Secret")
            secret_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.api_inputs[name] = (key_input, secret_input)

            row.addWidget(QLabel(name))
            row.addWidget(key_input)
            row.addWidget(secret_input)
            self.layout().addLayout(row)

        save_btn = QPushButton("✅ Save & Launch QuickTrade")
        save_btn.clicked.connect(self.save_and_close)
        self.layout().addWidget(save_btn)

    def save_and_close(self):
        selected = [name for name, cb in self.checkboxes.items() if cb.isChecked()]
        if not selected:
            QMessageBox.warning(self, "Setup Incomplete", "Please select at least one exchange.")
            return

        prefs = {"selected_exchanges": selected}
        with open(USER_PREFS_FILE, 'w') as f:
            json.dump(prefs, f, indent=4)

        api_keys = {}
        for name in selected:
            api_key, api_secret = self.api_inputs[name]
            api_keys[name] = {
                "api_key": api_key.text(),
                "api_secret": api_secret.text()
            }

        with open(API_KEYS_FILE, 'w') as f:
            json.dump(api_keys, f, indent=4)

        self.on_complete()
        self.close()
