import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load the token securely
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("\n🚨 ERROR: TELEGRAM_BOT_TOKEN is missing! Set it as an environment variable.")
    exit(1)

# Define command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your study bot. How can I help you today?")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("You can ask me anything related to studies!")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(f"You said: {text}")

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
