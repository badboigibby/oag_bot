import asyncio
import os
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import datetime

# Your bot token
BOT_TOKEN = "7745593859:AAH2fZCPD2F_55NLTG3ImO7O9F5MZcE1Ubo"
STORE_URL = "https://oag-store.onrender.com"

# Product list
PRODUCTS = [
    {
        "name": "Nike Mens Basketball Basketball Shoe",
        "price": "$515.69",
        "image": "https://m.media-amazon.com/images/I/61BU4ndeMlL._AC_SX575_.jpg",
        "link": "https://amzn.to/42bGc3C"
    },
    {
        "name": "Nike Mens Basketball Basketball Shoe",
        "price": "$389.51",
        "image": "https://m.media-amazon.com/images/I/71d4X0aGqwL._AC_SX575_.jpg",
        "link": "https://amzn.to/4haxIOf"
    },
    {
        "name": "Wkwmrpet Womens Oversized Crewneck Sweatshirts Long Sleeve Fleece Pullover Sweaters Casual Workout Tops Fall Winter Clothes",
        "price": "$40.99",
        "image": "https://m.media-amazon.com/images/I/81yTc9JggVL._AC_SX466_.jpg",
        "link": "https://amzn.to/4g8iBUF"
    },
    {
        "name": "Outdoor Ventures Men's Lightweight Softshell Jacket Fleece Lined Hooded Water Resistant Winter Hiking Windbreaker Jackets",
        "price": "$61.59",
        "image": "https://m.media-amazon.com/images/I/719AibNfs1L._AC_SX466_.jpg",
        "link": "https://amzn.to/4gYx7zG"
    },
    {
        "name": "Eniloyal Sweatshirt for Women Long Sleeve Crewneck Pullover Hoodies Shirts Loose Fall Tops Sweaters 2024 Trendy Clothes",
        "price": "$31.99",
        "image": "https://m.media-amazon.com/images/I/71GOHxmqFwL._AC_SY606_.jpg",
        "link": "https://amzn.to/40DEUwR"
    },
    {
        "name": "Libin Men's Lightweight Joggers",
        "price": "$33.98",
        "image": "https://m.media-amazon.com/images/I/716YYMwItdL._AC_SY741_.jpg",
        "link": "https://amzn.to/3WprFgS"
    }
]

# Betting tips
BET_TIPS = [
    "Today's tip: Team A will win the match.",
    "Today's tip: Bet on over 2.5 goals in the next match.",
    "Today's tip: Player X to score anytime."
]

# Initialize the Flask app
app = Flask(__name__)

# Define the route for the home page (Flask)
@app.route('/')
def home():
    return "Bot is running!"  # This message appears when the root URL is accessed

# Function to save user chat IDs
def save_chat_id(chat_id):
    file_path = "chat_ids.txt"
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")  # Create the file if it doesn't exist

    with open(file_path, "r") as file:
        saved_ids = file.read().splitlines()

    if str(chat_id) not in saved_ids:
        with open(file_path, "a") as file:
            file.write(f"{chat_id}\n")

# Welcome message and save chat ID
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)  # Save chat ID
    welcome_message = (
        "Welcome to OAG Store Bot! 👋\n"
        "Discover our amazing products and deals.\n"
        f"Visit our store here: {STORE_URL}\n"
        "\nUse /products to see our featured items.\n"
        "You can also ask me questions directly, and I'll try to help!"
    )
    await update.message.reply_text(welcome_message)

# Show product list
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for product in PRODUCTS:
        caption = (
            f"🛍️ *{product['name']}*\n"
            f"💵 Price: {product['price']}"
        )
        buttons = [
            [InlineKeyboardButton("🔗 Buy Now", url=product['link'])],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=product['image'],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# Handle general messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)  # Save chat ID

    # Simulate a response for the query
    response = f"🤖 You asked: '{query}'. Here is some information: [Google it](https://www.google.com/search?q={query.replace(' ', '+')})"
    await update.message.reply_text(response, parse_mode="Markdown")

# Send daily bet tips
async def send_bet_tip(context):
    chat_id = context.job.chat_id
    tip = BET_TIPS[context.job.context % len(BET_TIPS)]  # Rotate through tips
    await context.bot.send_message(chat_id=chat_id, text=tip)

# Subscribe to daily bet tips
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.application.job_queue.run_daily(
        send_bet_tip,
        time=datetime.time(hour=9, minute=0),  # Set to your preferred time
        chat_id=chat_id,
        name=str(chat_id),
        context=len(BET_TIPS)  # To rotate tips
    )
    await update.message.reply_text("You have subscribed to daily bet tips! 🎉")

# Flask thread runner
def run_flask():
    app.run(debug=True, use_reloader=False, threaded=True)

# Main entry point for the application
async def main():
    # Set up your bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("products", show_products))
    application.add_handler(CommandHandler("subscribe", subscribe))

    # Message handler for general questions
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot with polling
    await application.run_polling()

# Main entry point for the application
if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the Telegram bot in the asyncio event loop
    loop.create_task(main())

    # Keep the asyncio loop running
    loop.run_forever()
