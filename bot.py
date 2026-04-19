import requests
import yfinance as yf
import pandas as pd
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ✅ FUNCTION (PLACE HERE)
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })
    print(response.text)   # DEBUG OUTPUT

def get_data():
    return yf.download("^NSEI", period="5d", interval="5m")

def generate_signal(data):
    data['SMA5'] = data['Close'].rolling(5).mean()
    data['SMA20'] = data['Close'].rolling(20).mean()

    latest = data.iloc[-1]

    if latest['SMA5'] > latest['SMA20']:
        return "BUY 📈"
    else:
        return "SELL 📉"

# ✅ MAIN FUNCTION
def main():
    send_telegram("🚀 Bot started running")   # 🔥 DEBUG MESSAGE

    data = get_data()

    if data.empty:
        send_telegram("❌ Data fetch failed")
        return

    signal = generate_signal(data)
    price = data['Close'].iloc[-1]

    message = f"NIFTY SIGNAL\nPrice: {price:.2f}\nSignal: {signal}"
    send_telegram(message)

# ✅ ENTRY POINT (MUST EXIST)
if __name__ == "__main__":
    main()
