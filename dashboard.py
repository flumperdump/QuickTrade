from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QTableWidget, QTableWidgetItem, QTabWidget, QComboBox, QLineEdit,
    QHBoxLayout, QStackedWidget, QMessageBox, QGroupBox, QScrollArea, QFormLayout
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

        self.total_label = QLabel("💰 Total Asset Value: USD $0.00")
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout().addWidget(self.total_label)

        controls_layout = QHBoxLayout()
        self.dust_filter = QCheckBox("Show Dust (<$1)")
        self.dust_filter.setChecked(False)
        self.dust_filter.stateChanged.connect(self.update_table)

        self.refresh_button = QPushButton("🔁 Refresh Assets")
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
        self.total_label.setText(f"💰 Total Asset Value: USD ${total:,.2f}")

class ExchangeTab(QWidget):
    def __init__(self, name):
        super().__init__()
        self.exchange = name
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel(f"Trading Interface for {name}"))

        self.market_selector = QComboBox()
        self.market_selector.addItems(["BTC/USDT", "ETH/USDT", "SOL/USDT"])
        self.layout().addWidget(self.market_selector)

        self.order_type = QComboBox()
        self.order_type.addItems(["Market", "Limit"])
        self.order_type.setCurrentText("Market")
        self.layout().addWidget(self.order_type)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price (Limit Only)")
        self.layout().addWidget(self.price_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.layout().addWidget(self.amount_input)

        button_layout = QHBoxLayout()
        buy_button = QPushButton("Buy")
        sell_button = QPushButton("Sell")
        button_layout.addWidget(buy_button)
        button_layout.addWidget(sell_button)
        self.layout().addLayout(button_layout)

        buy_button.clicked.connect(lambda: self.simulate_trade("Buy"))
        sell_button.clicked.connect(lambda: self.simulate_trade("Sell"))

    def simulate_trade(self, side):
        pair = self.market_selector.currentText()
        order_type = self.order_type.currentText()
        price = self.price_input.text()
        amount = self.amount_input.text()

        if order_type == "Limit" and not price:
            QMessageBox.warning(self, "Missing Input", "Please enter a price for a Limit order.")
            return

        if not amount:
            QMessageBox.warning(self, "Missing Input", "Please enter an amount.")
            return

        QMessageBox.information(self, f"{side} Order", f"{side}ing {amount} {pair} as a {order_type} order on {self.exchange}.")

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container.setLayout(QVBoxLayout())

        self.api_keys = load_api_keys()
        self.user_prefs = load_user_prefs()
        self.selected_exchanges = self.user_prefs.get("selected_exchanges", EXCHANGES)

        container.layout().addWidget(QLabel("Edit API Keys:"))
        for exchange in EXCHANGES:
            exchange_box = QGroupBox(exchange)
            exchange_box.setCheckable(True)
            exchange_box.setChecked(exchange in self.selected_exchanges)
            exchange_box.setLayout(QVBoxLayout())

            exchange_keys = self.api_keys.get(exchange, {})
            for sub_label, creds in exchange_keys.items():
                sub_box = QGroupBox(sub_label)
                sub_box.setCheckable(True)
                sub_box.setChecked(False)
                sub_box.setLayout(QFormLayout())

                api_key_input = QLineEdit(creds.get("api_key", ""))
                api_secret_input = QLineEdit(creds.get("api_secret", ""))
                api_secret_input.setEchoMode(QLineEdit.EchoMode.Password)

                save_btn = QPushButton("Save")
                def save_sub_key(ex=exchange, sub=sub_label, k=api_key_input, s=api_secret_input):
                    if ex not in self.api_keys:
                        self.api_keys[ex] = {}
                    self.api_keys[ex][sub] = {"api_key": k.text(), "api_secret": s.text()}
                    save_api_keys(self.api_keys)
                    QMessageBox.information(self, "Saved", f"Keys for {ex} → {sub} saved.")

                save_btn.clicked.connect(save_sub_key)

                sub_box.layout().addRow("API Key:", api_key_input)
                sub_box.layout().addRow("API Secret:", api_secret_input)
                sub_box.layout().addRow(save_btn)

                exchange_box.layout().addWidget(sub_box)

            container.layout().addWidget(exchange_box)

        scroll_area.setWidget(container)
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade")
        self.resize(1024, 650)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard = DashboardTab()
        self.tabs.addTab(self.dashboard, "Dashboard")

        self.exchange_tabs = {}
        prefs = load_user_prefs()
        selected_exchanges = prefs.get("selected_exchanges", EXCHANGES)

        for name in selected_exchanges:
            tab = ExchangeTab(name)
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
