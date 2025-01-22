from flask import Flask
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import pytz

app = Flask(__name__)

# Reading the bot token from an environment variable
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

# Chat IDs to send tips to
CHAT_IDS = [123456789, 987654321, 1122334455]  # Replace with your actual chat IDs

# Frequently Asked Questions (FAQs)
FAQS = [
    {
        "question": "What is OAG Store?",
        "answer": "OAG Store is an online platform where you can find amazing products at great prices."
    },
    {
        "question": "How do I make a purchase?",
        "answer": "Visit our store by clicking on the product links provided and follow the checkout process."
    },
    {
        "question": "What is the return policy?",
        "answer": "You can return products within 30 days of purchase. Check our website for more details."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "Email us at support@oagstore.com. We aim to respond within 24 hours."
    }
]

# FAQ handler
async def show_faqs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs_message = "Here are some frequently asked questions:\n\n"
    for faq in FAQS:
        faqs_message += f"❓ {faq['question']}\n💬 {faq['answer']}\n\n"
    await update.message.reply_text(faqs_message)

# Function to send daily tips
async def send_tips(context: ContextTypes.DEFAULT_TYPE):
    message = "Here are your daily tips for betting. Good luck!"
    for chat_id in CHAT_IDS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Error sending message to chat ID {chat_id}: {e}")

# Main function to initialize and run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add a command handler for FAQs
    application.add_handler(CommandHandler("faqs", show_faqs))

    # Schedule daily tips at a specific time
    job_queue = application.job_queue
    timezone = pytz.timezone("America/Edmonton")  # Set your local timezone
    target_time = datetime.time(hour=9, minute=0, tzinfo=timezone)  # Schedule for 9:00 AM
    job_queue.run_daily(send_tips, time=target_time)

    # Start the application
    application.run_polling()

if __name__ == "__main__":
    main()
