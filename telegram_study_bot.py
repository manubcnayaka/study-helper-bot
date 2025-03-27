import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text("Hello! I am your Study Helper Bot. Ask me any 10th or 2nd PUC question!")


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user messages and get answers from OpenAI."""
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        answer = response["choices"][0]["message"]["content"]
    except Exception as e:
        answer = "Sorry, I couldn't process your request."

    await update.message.reply_text(answer)


def main():
    """Main function to run the bot."""
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
