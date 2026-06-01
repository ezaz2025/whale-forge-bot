import telebot
import requests
from datetime import datetime
from flask import Flask
from threading import Thread

# =========================================
# BOT TOKEN
# =========================================

TOKEN = "8906538078:AAGgeXgItJTrkwHmii0fF3J9kE-Sr7o4vsE"

# =========================================
# COINGECKO API KEY
# =========================================

API_KEY = "CG-qFVb3uzSANjMmWopxQUiPVjC"

# =========================================
# START BOT
# =========================================

bot = telebot.TeleBot(TOKEN)

# =========================================
# FLASK SERVER FOR RENDER
# =========================================

app = Flask('')

@app.route('/')
def home():
    return "Whale Forge Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=10000)

t = Thread(target=run)
t.start()

# =========================================
# START MESSAGE
# =========================================

@bot.message_handler(commands=['start'])
def start(message):

    text = f"""
🐋 Welcome to Whale Forge

📊 Track any crypto instantly.

Examples:
• btc
• 0.01 btc
• 10 btc
• eth
• 0.76 sol

⚡ Powered by Crypto Lab
👑 Owner: Ezaz
"""

    bot.reply_to(message, text)

# =========================================
# TRACKER
# =========================================

@bot.message_handler(func=lambda message: True)
def tracker(message):

    try:

        text = message.text.lower().strip().split()

        if len(text) == 2:
            amount = float(text[0])
            coin = text[1]
        else:
            amount = 1
            coin = text[0]

        url = f"https://api.coingecko.com/api/v3/coins/{coin}"

        headers = {
            "x-cg-demo-api-key": API_KEY
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if 'market_data' not in data:
            raise Exception("Coin not found")

        name = data['name']
        symbol = data['symbol'].upper()

        price = data['market_data']['current_price']['usd']
        marketcap = data['market_data']['market_cap']['usd']
        change = data['market_data']['price_change_percentage_24h']

        ath = data['market_data']['ath']['usd']
        atl = data['market_data']['atl']['usd']

        rank = data['market_cap_rank']

        total_value = amount * price

        time_now = datetime.now().strftime("%I:%M %p")

        msg = f"""
🐋 Whale Forge

🪙 Coin: {name} ({symbol})

💰 1 {symbol} = ${price:,.4f}

🧮 {amount} {symbol} = ${total_value:,.4f}

📈 24h Change: {change:.2f}%
🏆 Rank: #{rank}

🚀 ATH: ${ath:,.2f}
📉 ATL: ${atl:,.4f}

💎 Market Cap:
${marketcap:,.0f}

🕒 Updated:
{time_now}

👑 Owner: Ezaz
"""

        bot.reply_to(message, msg)

    except:

        bot.reply_to(
            message,
            "⚠️ Coin not found.\n\nExamples:\nbtc\n0.01 btc\n10 eth"
        )

# =========================================
# RUN BOT
# =========================================

print("✅ Whale Forge Online")

bot.infinity_polling()