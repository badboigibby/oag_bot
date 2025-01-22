from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set!")
