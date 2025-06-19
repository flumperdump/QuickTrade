from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabBar,
    QStackedLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QStackedWidget
)
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade - Manual Trading Companion for SIGNUM")
        self.setGeometry(100, 100, 1080, 720)
        self.setStyleSheet(self.get_stylesheet())

        self.init_ui()

    def init_ui(self):
        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top navigation
        self.tabs = QTabBar()
        self.tabs.addTab("Dashboard")
        self.tabs.addTab("Binance")
        self.tabs.addTab("Kraken")
        self.tabs.addTab("KuCoin")
        self.tabs.addTab("Settings")
        self.tabs.setMovable(False)
        self.tabs.setDrawBase(False)
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 120px; }")

        self.tabs.currentChanged.connect(self.switch_tab)

        # Content area
        self.stack = QStackedWidget()
        self.stack.addWidget(self.build_dashboard())
        self.stack.addWidget(self.build_exchange_tab("Binance"))
        self.stack.addWidget(self.build_exchange_tab("Kraken"))
        self.stack.addWidget(self.build_exchange_tab("KuCoin"))
        self.stack.addWidget(self.build_settings())

        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.stack)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def build_dashboard(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("💰 Dashboard – Total Asset Value: $xx,xxx.xx")
        label.setFont(QFont("Segoe UI", 16))
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def build_exchange_tab(self, name):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"🔁 {name} Manual Trading Interface (Coming Soon)"))
        widget.setLayout(layout)
        return widget

    def build_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙️ Settings – API Keys, Preferences"))
        widget.setLayout(layout)
        return widget

    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #0d1117;
            }
            QTabBar::tab {
                background: #1b1f27;
                color: #ffffff;
                border: 1px solid #1b74e4;
                padding: 8px;
                margin-right: 4px;
                font: 12pt "Segoe UI";
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #2d9cdb;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font: 11pt "Segoe UI";
            }
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
