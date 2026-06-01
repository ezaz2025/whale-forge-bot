import telebot
import requests
from datetime import datetime

# =====================================
# BOT TOKEN
# =====================================
TOKEN = "8906538078:AAHC-euZglqaydXPjgeWT-YoJSi1NeErPB8"

# =====================================
# COINGECKO API KEY
# =====================================
API_KEY = "CG-qFVb3uzSANjMmWopxQUiPVjC"

# =====================================
# START BOT
# =====================================
bot = telebot.TeleBot(TOKEN)

# =====================================
# START COMMAND
# =====================================
@bot.message_handler(commands=['start'])
def start(message):

    text = """
╔══════════════╗
   🐋 Whale Forge
╚══════════════╝

Advanced Crypto Tracking Agent

━━━━━━━━━━━━━━

📥 Examples

• 0.005 eth
• 100 doge
• 500 pepe
• 2 trump
• 1 btc

━━━━━━━━━━━━━━

⚡ Powered by CoinGecko
"""

    bot.reply_to(message, text)

# =====================================
# HELP COMMAND
# =====================================
@bot.message_handler(commands=['help'])
def help_command(message):

    text = """
📊 HOW TO USE

Send amount + coin symbol

Examples:

• 0.5 eth
• 100 doge
• 50 shib

━━━━━━━━━━━━━━

🌐 Supports thousands of coins
"""

    bot.reply_to(message, text)

# =====================================
# MAIN TRACKER
# =====================================
@bot.message_handler(func=lambda message: True)
def tracker(message):

    try:

        text = message.text.lower().strip()

        parts = text.split()

        if len(parts) != 2:

            bot.reply_to(
                message,
                "⚠️ Invalid format\nExample: 0.005 eth"
            )

            return

        amount = float(parts[0])

        symbol = parts[1]

        # =====================================
        # SEARCH COIN
        # =====================================
        headers = {
            "x-cg-demo-api-key": API_KEY
        }

        search_url = f"https://api.coingecko.com/api/v3/search?query={symbol}"

        search_data = requests.get(
            search_url,
            headers=headers
        ).json()

        coins = search_data.get("coins")

        if not coins:

            bot.reply_to(
                message,
                "❌ Coin not found"
            )

            return

        coin_id = coins[0]["id"]
        coin_name = coins[0]["name"]
        coin_symbol = coins[0]["symbol"].upper()

        # =====================================
        # GET PRICE
        # =====================================
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

        price_data = requests.get(
            price_url,
            headers=headers
        ).json()

        price = price_data[coin_id]["usd"]

        total = amount * price

        current_time = datetime.now().strftime("%I:%M %p")

        # =====================================
        # REPLY
        # =====================================
        reply = f"""
╔══════════════╗
   💠 Whale Report
╚══════════════╝

🪙 Asset
{coin_name} ({coin_symbol})

📦 Amount
{amount}

💵 USD Value
${total:,.4f}

━━━━━━━━━━━━━━

🕒 {current_time}

⚡ CoinGecko Live Data
"""

        bot.reply_to(message, reply)

    except Exception as e:

        print(e)

        bot.reply_to(
            message,
            "⚠️ Invalid request"
        )

# =====================================
# RUN BOT
# =====================================
print("✅ Whale Forge Online")

bot.infinity_polling()