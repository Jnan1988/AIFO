import requests
import yfinance as yf
import pandas as pd
import os
import time

# Load environment variables from GitHub Secrets
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        print("Error: TOKEN or CHAT_ID not found in environment variables.")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        print(f"Telegram response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send Telegram: {e}")

def get_data():
    print("Fetching data from NSE...")
    # Fetching 5-day history to ensure enough data for 20-period SMA
    data = yf.download("^NSEI", period="5d", interval="5m", auto_adjust=True)
    
    # ✅ FIX FOR 2026 MULTI-INDEX ERROR
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    return data

def generate_signal(data):
    # Calculate Simple Moving Averages
    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()

    # Get the last two rows to check for a "Crossover"
    if len(data) < 20:
        return "WAIT (Not enough data)"

    latest = data.iloc[-1]
    
    if latest['SMA5'] > latest['SMA20']:
        return "BUY 📈 (Bullish Crossover)"
    else:
        return "SELL 📉 (Bearish Trend)"

def main():
    print("Bot execution started...")
    data = get_data()

    if data.empty:
        send_telegram("❌ *Data fetch failed:* Yahoo Finance returned no data.")
        return

    signal = generate_signal(data)
    price = data['Close'].iloc[-1]

    message = f"🔔 *NIFTY 50 SIGNAL*\n💰 *Price:* {price:.2f}\n📊 *Action:* {signal}"
    print(message)
    send_telegram(message)

if __name__ == "__main__":
    main()
