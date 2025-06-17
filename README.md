# 🚀 QuickTrade – Manual Crypto Trading Companion for SIGNUM

QuickTrade is a lightweight, privacy-first Windows desktop app that allows SIGNUM users to manually trade cryptocurrencies across multiple exchanges using subaccount API keys — **without coding, scripting, or logging into exchange websites**.

> 🎯 Designed for intuitive manual control and overrides of automated bots, with full support for subaccount management.

---

## 🧩 Features

- ✅ **Manual Market Trades** on supported exchanges
- 🔐 **Local-only API key storage** (AES encryption-ready)
- 🌘 **Dark-mode native**, SIGNUM-inspired UI
- 🪙 **Real-time asset value dashboard**
- 🔄 **Multi-exchange support**: Bybit, Kraken, Binance, KuCoin, Coinbase, MEXC, Bitget, Crypto.com, Hyperliquid
- 💾 **Auto-saves user preferences** (selected exchange, subaccount, currency)
- ⚙️ **Easy API key management** (edit/update securely via UI)
- 🧠 Architected for future support of:
  - Limit orders
  - Order history logging
  - Multi-language UI
  - Manual trade override logs

---

## 💻 Installation (Windows)

> 📦 No Python required. This is a standalone installer.

1. Go to the **[Releases tab](../../releases)** or download directly:
   - 👉 [Download QuickTrade_v1.0_Package.zip](../../releases)
2. Extract the `.zip` file anywhere (e.g., Desktop or Documents)
3. Run `QuickTradeInstaller_v1.0.exe`
4. Follow the **Setup Wizard** — no technical steps required
5. Launch `QuickTrade` from your Start Menu or Desktop shortcut

---

## 🛠 Initial Setup Instructions

### 🧪 1. Choose Exchanges
During first launch, select the exchanges you use (e.g. Binance, Kraken).

### 🔑 2. Enter API Keys
For each exchange and subaccount you select:
- Click "Edit API Keys"
- Paste your **API Key** and **Secret**
- Save securely — stored only on your device in `config/api_keys.json`

### 📈 3. Explore the Dashboard
See your total asset value, balances, and manually place market trades.

---

## 🔐 Privacy & Security

- All data is stored **locally** on your machine (`config/` folder)
- No telemetry, cloud sync, or internet logging
- AES encryption can be enabled in future versions (optional)

---

## 📁 Folder Structure

QuickTrade/
├── config/
│ ├── api_keys.json
│ └── user_prefs.json
├── QuickTrade.exe
├── README.txt
└── assets/

---

## 🧠 Coming Soon

- ✅ Limit Order Support
- ✅ Order History Logging
- ✅ Override Indicators for Bot Interruption
- ✅ Enhanced Logging (manual vs. auto trades)
- ✅ Mac & Linux versions

---

## 🙋 Support

Have questions or ideas for improvements?
- Submit an issue here on GitHub
- Or reach out via the [Signum community](https://signumtrading.ai)

---

## 🧑‍💻 Built With

- [PyQt6](https://pypi.org/project/PyQt6/)
- [Requests](https://pypi.org/project/requests/)
- [pycoingecko](https://pypi.org/project/pycoingecko/) *(optional for price caching)*
- [pycryptodome](https://pypi.org/project/pycryptodome/) *(planned for encryption)*

---

## 🧢 Credits

QuickTrade was built as an unofficial companion to the SIGNUM Trading Platform by professional developers and AI collaborators. It is not affiliated with SIGNUM but shares the design aesthetic and purpose.

---

## 📜 License

MIT License – use, share, or fork as you wish!

