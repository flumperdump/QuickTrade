from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QDialogButtonBox, QGridLayout, QLineEdit, QGroupBox
)
import json
import os

CONFIG_PATH = "config/user_prefs.json"
API_KEYS_PATH = "config/api_keys.json"

SUPPORTED_EXCHANGES = [
    "Bybit", "Kraken", "Binance", "KuCoin", "Coinbase", "MEXC",
    "Bitget", "Crypto.com", "Hyperliquid"
]

class InitialSetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade - Initial Setup")
        self.setMinimumWidth(400)

        self.selected_exchanges = []
        self.api_inputs = {}

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select exchanges to enable:"))
        self.checkboxes = {}
        for ex in SUPPORTED_EXCHANGES:
            cb = QCheckBox(ex)
            cb.stateChanged.connect(self.toggle_api_inputs)
            layout.addWidget(cb)
            self.checkboxes[ex] = cb

        self.api_group = QGroupBox("API Keys (optional, can be added later)")
        self.api_layout = QGridLayout()
        self.api_group.setLayout(self.api_layout)
        layout.addWidget(self.api_group)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.save_and_close)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def toggle_api_inputs(self):
        for i in reversed(range(self.api_layout.count())):
            self.api_layout.itemAt(i).widget().deleteLater()
        self.api_inputs.clear()

        row = 0
        for ex, cb in self.checkboxes.items():
            if cb.isChecked():
                key_input = QLineEdit()
                key_input.setPlaceholderText("API Key")
                secret_input = QLineEdit()
                secret_input.setPlaceholderText("API Secret")
                secret_input.setEchoMode(QLineEdit.EchoMode.Password)

                self.api_layout.addWidget(QLabel(f"{ex} Key:"), row, 0)
                self.api_layout.addWidget(key_input, row, 1)
                row += 1
                self.api_layout.addWidget(QLabel(f"{ex} Secret:"), row, 0)
                self.api_layout.addWidget(secret_input, row, 1)
                row += 1

                self.api_inputs[ex] = {"key": key_input, "secret": secret_input}

    def save_and_close(self):
        selected = [ex for ex, cb in self.checkboxes.items() if cb.isChecked()]
        os.makedirs("config", exist_ok=True)

        # Save exchanges
        with open(CONFIG_PATH, 'w') as f:
            json.dump({"enabled_exchanges": selected}, f, indent=2)

        # Save API keys if provided
        api_data = {}
        for ex in selected:
            inputs = self.api_inputs.get(ex)
            if inputs:
                key = inputs["key"].text().strip()
                secret = inputs["secret"].text().strip()
                if key and secret:
                    api_data[ex] = {"api_key": key, "api_secret": secret}

        with open(API_KEYS_PATH, 'w') as f:
            json.dump(api_data, f, indent=2)

        self.accept()
