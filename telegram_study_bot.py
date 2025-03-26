import os
import json
import openai
import firebase_admin
import logging
from firebase_admin import credentials, firestore
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# Initialize Firebase
cred = credentials.Certificate(json.loads(FIREBASE_CREDENTIALS))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get answer from Firebase
def get_answer_from_firestore(question):
    doc_ref = db.collection("academic_questions").document(question.lower())
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("answer")
    return None

# Function to generate answer from OpenAI
def get_answer_from_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Telegram command: Start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm Study Helper Bot. Ask me any academic question!")

# Handle text messages
def handle_message(update: Update, context: CallbackContext) -> None:
    question = update.message.text
    answer = get_answer_from_firestore(question)
    
    if not answer:
        answer = get_answer_from_openai(question)
        # Store in Firebase for future reference
        db.collection("academic_questions").document(question.lower()).set({"answer": answer})
    
    update.message.reply_text(answer)

# Main function
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
