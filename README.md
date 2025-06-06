# ⛽  Ozen Telegram Crypto Gas Fee Bot

A powerful and easy-to-use Telegram bot that helps users track Ethereum and multi-chain gas prices, calculate manual transaction fees, and receive gas drop alerts — right from Telegram!


link- (https://t.me/Ozengasbot)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🚀 Features

- ✅ Get current Ethereum gas price with `/gas`
- ✅ Compare gas prices on Ethereum, BNB, and Polygon with `/multigas`
- ✅ Calculate manual gas fee in ETH and USD using `/calculate gasLimit gasPrice`
- ✅ Set an alert for low gas prices with `/setalert Gwei`
- ✅ Real-time ETH to USD conversion
- ✅ Background checker that notifies users when gas drops
- ✅ Fully Telegram-native interface (no website needed)
- ✅ Async-based architecture using `python-telegram-bot v20+`
- ✅ Easily extendable for more chains and utilities

---

## 📦 Tech Stack

- **Python 3.10+**
- **python-telegram-bot v20+**
- **Flask (optional, for Replit uptime)**
- **Requests (for API calls)**
- **Etherscan, BscScan, PolygonScan APIs**
- **CoinGecko API** for live ETH/USD rate

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gas-fee-bot.git
cd gas-fee-bot
