from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class ExchangeTab(QWidget):
    def __init__(self, exchange_name):
        super().__init__()
        self.exchange = exchange_name

        layout = QVBoxLayout()

        # Market selector
        self.market_selector = QComboBox()
        self.market_selector.addItems(["BTC/USDT", "ETH/USDT", "SOL/USDT"])
        layout.addWidget(self.market_selector)

        # Order type dropdown
        self.order_type = QComboBox()
        self.order_type.addItems(["Market", "Limit"])
        self.order_type.setCurrentText("Market")
        self.order_type.currentTextChanged.connect(self.toggle_price_field)
        layout.addWidget(self.order_type)

        # Price input (only shown when Limit is selected)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price (Limit Only)")
        self.price_input.setVisible(False)
        layout.addWidget(self.price_input)

        # Amount input
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(self.amount_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.buy_button = QPushButton("Buy")
        self.sell_button = QPushButton("Sell")
        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.sell_button)
        layout.addLayout(button_layout)

        self.buy_button.clicked.connect(lambda: self.simulate_trade("Buy"))
        self.sell_button.clicked.connect(lambda: self.simulate_trade("Sell"))

        self.setLayout(layout)

    def toggle_price_field(self, text):
        self.price_input.setVisible(text == "Limit")

    def simulate_trade(self, side):
        pair = self.market_selector.currentText()
        order_type = self.order_type.currentText()
        price = self.price_input.text().strip()
        amount = self.amount_input.text().strip()

        if order_type == "Limit" and not price:
            QMessageBox.warning(self, "Missing Input", "Please enter a price for a Limit order.")
            return

        if not amount:
            QMessageBox.warning(self, "Missing Input", "Please enter an amount.")
            return

        QMessageBox.information(
            self,
            f"{side} Order",
            f"{side}ing {amount} {pair} as a {order_type} order on {self.exchange}."
        )
