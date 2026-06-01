import telebot
import requests
from flask import Flask
from threading import Thread

# =====================================
# BOT TOKEN
# =====================================

TOKEN = "8906538078:AAGgeXgItJTrkwHmii0fF3J9kE-Sr7o4vsE"

# =====================================
# COINGECKO API
# =====================================

COINGECKO_API_KEY = "CG-qFVb3uzSANjMmWopxQUiPVjC"

# =====================================
# BOT START
# =====================================

bot = telebot.TeleBot(TOKEN)

# =====================================
# FLASK SERVER
# =====================================

app = Flask('')

@app.route('/')
def home():
    return "Whale Forge Bot Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# =====================================
# START COMMAND
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
# CRYPTO PRICE SYSTEM
# =====================================

@bot.message_handler(func=lambda message: True)
def crypto_price(message):

    try:
        user_input = message.text.lower().strip()

        parts = user_input.split()

        # DEFAULT VALUES
        amount = 1

        # IF USER TYPES:
        # btc
        # 0.01 btc
        # 10 eth

        try:
            amount = float(parts[0])
            coin_query = parts[1]
        except:
            coin_query = parts[0]

        # =====================================
        # API HEADERS
        # =====================================

        headers = {
            "x-cg-demo-api-key": COINGECKO_API_KEY
        }

        # =====================================
        # SEARCH COIN
        # =====================================

        search_url = f"https://api.coingecko.com/api/v3/search?query={coin_query}"

        search_data = requests.get(
            search_url,
            headers=headers
        ).json()

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

        # =====================================
        # GET LIVE PRICE
        # =====================================

        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

        price_data = requests.get(
            price_url,
            headers=headers
        ).json()

        if coin_id not in price_data:
            bot.reply_to(
                message,
                "⚠️ Price unavailable right now."
            )
            return

        current_price = price_data[coin_id]["usd"]

        total_value = current_price * amount

        # =====================================
        # FINAL REPLY
        # =====================================

        reply = f"""
💎 {coin_name} ({coin_symbol})

💰 Amount: {amount}

📊 Price: ${current_price:,.4f}

💵 Total Value: ${total_value:,.4f}

⚡ Powered by CoinGecko
"""

        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(
            message,
            f"⚠️ Error: {str(e)}"
        )

# =========================
# RUN BOT
# =========================

def run_bot():
    print("✅ Whale Forge Online")
    bot.infinity_polling()

Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=8080)