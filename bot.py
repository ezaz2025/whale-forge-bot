import telebot
import requests
from datetime import datetime
from flask import Flask
from threading import Thread

# =====================================
# BOT TOKEN
# =====================================

TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(TOKEN)

# =====================================
# KEEP RENDER ONLINE
# =====================================

app = Flask('')

@app.route('/')
def home():
    return "Whale Forge Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# =====================================
# START MESSAGE
# =====================================

@bot.message_handler(commands=['start'])
def start(message):

    text = """
🐋 Welcome to Whale Forge

📈 Track crypto prices whenever you want.

Supported Examples:
• BTC
• ETH
• SOL
• XRP

⚡ Live Market Data
👑 Owner: Ezaz
"""

    bot.reply_to(message, text)

# =====================================
# MAIN PRICE SYSTEM
# =====================================

@bot.message_handler(func=lambda message: True)
def crypto_price(message):

    try:

        user_input = message.text.lower().strip()
        parts = user_input.split()

        amount = 1
        coin_query = ""

        # -----------------------------
        # INPUT DETECTION
        # -----------------------------

        if len(parts) == 1:

            try:
                float(parts[0])

                bot.reply_to(
                    message,
                    "⚠️ Please enter a coin symbol.\nExample: BTC"
                )
                return

            except:
                coin_query = parts[0]

        elif len(parts) >= 2:

            try:
                amount = float(parts[0])
                coin_query = parts[1]

            except:
                coin_query = parts[0]

        # -----------------------------
        # SEARCH COIN FROM COINGECKO
        # -----------------------------

        search_url = f"https://api.coingecko.com/api/v3/search?query={coin_query}"

        search_data = requests.get(search_url).json()

        if not search_data.get("coins"):

            bot.reply_to(
                message,
                "⚠️ Coin not found.\nTry another symbol."
            )
            return

        coin = search_data["coins"][0]

        coin_id = coin["id"]
        coin_name = coin["name"]
        coin_symbol = coin["symbol"].upper()

        # -----------------------------
        # GET LIVE PRICE
        # -----------------------------

        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

        price_data = requests.get(price_url).json()

        if coin_id not in price_data:

            bot.reply_to(
                message,
                "⚠️ Price unavailable right now."
            )
            return

        current_price = price_data[coin_id]["usd"]

        total_value = current_price * amount

        # -----------------------------
        # FINAL REPLY
        # -----------------------------

        reply = f"""
💰 {amount} {coin_symbol}

💵 USD Value: ${total_value:,.4f}

📈 Current Price:
1 {coin_symbol} = ${current_price:,.4f}

🪙 {coin_name}

🕒 {datetime.now().strftime('%I:%M %p')}

⚡ Powered by CoinGecko
"""

        bot.reply_to(message, reply)

    except:

        bot.reply_to(
            message,
            "⚠️ Something went wrong.\nPlease try again."
        )

# =====================================
# RUN BOT
# =====================================

print("✅ Whale Forge Online")

bot.infinity_polling()