from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QTableWidget, QTableWidgetItem, QTabWidget, QComboBox, QLineEdit,
    QHBoxLayout, QStackedWidget, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
import sys
import json
import os
import time
import random

CONFIG_PATH = "config"
API_KEYS_FILE = os.path.join(CONFIG_PATH, "api_keys.json")
USER_PREFS_FILE = os.path.join(CONFIG_PATH, "user_prefs.json")

EXCHANGES = ["Bybit", "Kraken", "Binance", "KuCoin", "Coinbase", "MEXC", "Bitget", "Crypto.com", "Hyperliquid"]

os.makedirs(CONFIG_PATH, exist_ok=True)

def load_user_prefs():
    if os.path.exists(USER_PREFS_FILE):
        with open(USER_PREFS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_prefs(prefs):
    with open(USER_PREFS_FILE, 'w') as f:
        json.dump(prefs, f, indent=4)

def load_api_keys():
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_api_keys(keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.total_label = QLabel("\ud83d\udcb0 Total Asset Value: USD $0.00")
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout().addWidget(self.total_label)

        controls_layout = QHBoxLayout()
        self.dust_filter = QCheckBox("Show Dust (<$1)")
        self.dust_filter.setChecked(False)
        self.dust_filter.stateChanged.connect(self.update_table)

        self.refresh_button = QPushButton("\ud83d\udd01 Refresh Assets")
        self.refresh_button.clicked.connect(self.load_balances)

        controls_layout.addWidget(self.dust_filter)
        controls_layout.addWidget(self.refresh_button)
        controls_layout.addStretch()
        self.layout().addLayout(controls_layout)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Exchange", "Subaccount", "Asset", "Balance (USD)"])
        self.layout().addWidget(self.table)

        self.balances = []
        self.load_balances()

    def load_balances(self):
        self.balances = [
            {"exchange": "Binance", "subaccount": "Main", "asset": "BTC", "usd_value": 23450.12},
            {"exchange": "Kraken", "subaccount": "Bot1", "asset": "ETH", "usd_value": 1345.33},
            {"exchange": "KuCoin", "subaccount": "Main", "asset": "DOGE", "usd_value": 0.52},
            {"exchange": "Bybit", "subaccount": "Alt", "asset": "SOL", "usd_value": 85.22}
        ]
        self.update_table()

    def update_table(self):
        show_dust = self.dust_filter.isChecked()
        filtered = [b for b in self.balances if show_dust or b["usd_value"] >= 1.0]
        self.table.setRowCount(len(filtered))
        total = 0.0
        for i, b in enumerate(filtered):
            self.table.setItem(i, 0, QTableWidgetItem(b["exchange"]))
            self.table.setItem(i, 1, QTableWidgetItem(b["subaccount"]))
            self.table.setItem(i, 2, QTableWidgetItem(b["asset"]))
            self.table.setItem(i, 3, QTableWidgetItem(f"${b['usd_value']:.2f}"))
            total += b["usd_value"]
        self.total_label.setText(f"\ud83d\udcb0 Total Asset Value: USD ${total:,.2f}")

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.api_keys = load_api_keys()
        self.user_prefs = load_user_prefs()
        self.selected_exchanges = self.user_prefs.get("selected_exchanges", EXCHANGES)
        self.build_ui()

    def build_ui(self):
        self.layout().addWidget(QLabel("Edit API Keys:"))
        for exchange in self.selected_exchanges:
            box = QGroupBox(exchange)
            box.setLayout(QVBoxLayout())

            key_field = QLineEdit(self.api_keys.get(exchange, {}).get("api_key", ""))
            key_field.setPlaceholderText("API Key")
            secret_field = QLineEdit(self.api_keys.get(exchange, {}).get("api_secret", ""))
            secret_field.setPlaceholderText("API Secret")
            secret_field.setEchoMode(QLineEdit.EchoMode.Password)

            save_btn = QPushButton("Save")
            def save_key(exchange=exchange, key_field=key_field, secret_field=secret_field):
                self.api_keys[exchange] = {
                    "api_key": key_field.text(),
                    "api_secret": secret_field.text()
                }
                save_api_keys(self.api_keys)
                QMessageBox.information(self, "Saved", f"API keys for {exchange} saved.")

            save_btn.clicked.connect(save_key)

            box.layout().addWidget(key_field)
            box.layout().addWidget(secret_field)
            box.layout().addWidget(save_btn)
            self.layout().addWidget(box)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade")
        self.resize(1024, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard = DashboardTab()
        self.tabs.addTab(self.dashboard, "Dashboard")

        self.exchange_tabs = {}
        prefs = load_user_prefs()
        selected_exchanges = prefs.get("selected_exchanges", EXCHANGES)

        for name in selected_exchanges:
            tab = QWidget()
            tab.setLayout(QVBoxLayout())
            tab.layout().addWidget(QLabel(f"Trading UI for {name} will be here"))
            self.exchange_tabs[name] = tab
            self.tabs.addTab(tab, name)

        self.settings_tab = SettingsTab()
        self.tabs.addTab(self.settings_tab, "Settings")

        self.tabs.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
