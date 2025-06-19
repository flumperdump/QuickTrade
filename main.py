from PyQt6.QtWidgets import QApplication
import sys
from dashboard import DashboardTab
from settings_ui import SettingsTab  # if separated, else remove this line
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from utils import load_user_prefs  # wherever your prefs are stored
from exchange_tab import ExchangeTab  # this assumes exchange tabs are in their own file

EXCHANGES = ["Bybit", "Kraken", "Binance", "KuCoin", "Coinbase", "MEXC", "Bitget", "Crypto.com", "Hyperliquid"]

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
