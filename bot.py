send_telegram("🚀 Bot started running")
import requests
import yfinance as yf
import pandas as pd
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

try:
    data = yf.download("^NSEI", period="5d", interval="5m")

    if data.empty:
        send_telegram("❌ No data received from market")
        exit()

    data['SMA5'] = data['Close'].rolling(5).mean()
    data['SMA20'] = data['Close'].rolling(20).mean()

    latest = data.iloc[-1]

    if latest['SMA5'] > latest['SMA20']:
        signal = "BUY 📈"
    else:
        signal = "SELL 📉"

    msg = f"NIFTY SIGNAL\nPrice: {latest['Close']:.2f}\nSignal: {signal}"
    send_telegram(msg)

except Exception as e:
    send_telegram(f"❌ ERROR: {str(e)}")
