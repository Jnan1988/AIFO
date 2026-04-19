import requests
import yfinance as yf
import pandas as pd
import os

# --- TELEGRAM SETTINGS ---
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# --- STOCK SYMBOL ---
SYMBOL = "^NSEI"  # Nifty 50

def get_data():
    data = yf.download(SYMBOL, period="1d", interval="5m")
    return data

def generate_signal(data):
    data['SMA_5'] = data['Close'].rolling(5).mean()
    data['SMA_20'] = data['Close'].rolling(20).mean()

    latest = data.iloc[-1]

    if latest['SMA_5'] > latest['SMA_20']:
        return "BUY 📈"
    elif latest['SMA_5'] < latest['SMA_20']:
        return "SELL 📉"
    else:
        return "HOLD ⏸️"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def main():
    data = get_data()

    if data.empty:
        send_telegram("❌ Data fetch failed")
        return

    signal = generate_signal(data)
    price = data['Close'].iloc[-1]

    message = f"""
📊 NIFTY SIGNAL
Price: {price:.2f}
Signal: {signal}
"""

    send_telegram(message)

if __name__ == "__main__":
    main()
