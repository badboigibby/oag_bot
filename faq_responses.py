from telegram import Update
from telegram.ext import ContextTypes

FAQ_ANSWERS = {
    "what is oag store?": "OAG Store is your one-stop shop for amazing products and deals. Check it out at: https://oag-store.onrender.com",
    "how to buy products?": "You can browse and purchase products directly from our website. Use the /products command to see featured items.",
    "subscribe to tips": "You can subscribe to daily betting tips using the /subscribe command.",
}

# Function to get FAQ response based on query
def get_faq_response(query):
    query = query.lower().strip()
    
    # Try to find a matching FAQ answer
    for key in FAQ_ANSWERS:
        if key in query:  # Check for partial matches
            return FAQ_ANSWERS[key]
    
    return "Sorry, I couldn't find an answer to your question. Try asking something else!"

# Function to handle the user's message and respond
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    faq_response = get_faq_response(user_message)

    await update.message.reply_text(faq_response)
