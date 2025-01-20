from flask import Flask
import os

app = Flask(__name__)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot import start, show_products
import datetime
import pytz

import os

# Your token from environment variable
token = os.getenv("TELEGRAM_BOT_TOKEN")

# Your bot setup and other code here


# Chat IDs to send tips to
CHAT_IDS = [123456789, 987654321, 1122334455]  # Replace with your actual chat IDs

# Frequently Asked Questions (FAQs)
FAQS = [
    {
        "question": "What is OAG Store?",
        "answer": "OAG Store is an online platform where you can find amazing products at great prices. We offer various deals and discounts on a wide range of items."
    },
    {
        "question": "How do I make a purchase?",
        "answer": "To make a purchase, simply visit our store by clicking on the product links provided, select your items, and follow the checkout process."
    },
    {
        "question": "What is the return policy?",
        "answer": "Our return policy allows you to return products within 30 days of purchase. Please check our website for more detailed information on the return procedure."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can reach our customer support team via email at support@oagstore.com. We aim to respond within 24 hours."
    }
]

# FAQ handler
async def show_faqs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs_message = "Here are some frequently asked questions:\n\n"
    
    for faq in FAQS:
        faqs_message += f"❓ *{faq['question']}*\n"
        faqs_message += f"💬 *Answer:* {faq['answer']}\n\n"
    
    await update.message.reply_text(faqs_message, parse_mode="MarkdownV2")

# Function to send daily tips
async def send_tips(context: ContextTypes.DEFAULT_TYPE):
    message = "Here are your daily tips for betting. Good luck!"
    for chat_id in CHAT_IDS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Error sending message to chat ID {chat_id}: {e}")

# Main function to run the bot
def main():
    # Bot token (replace with your actual bot token)
    token = "7745593859:AAGBbhDdDK_nKIDz7ZD_kdXwNzLxauhA4YQ"

    # Create the application (this is the entry point of your bot)
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("products", show_products))
    application.add_handler(CommandHandler("faq", show_faqs))  # Add the FAQ command

    # Schedule daily tips at 1:00 AM MST
    mst = pytz.timezone("America/Edmonton")  # Mountain Standard Time
    application.job_queue.run_daily(send_tips, time=datetime.time(1, 0, tzinfo=mst))

    # Start the bot
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
