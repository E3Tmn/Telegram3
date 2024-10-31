from dotenv import load_dotenv
import os
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext
from intent import detect_intent_texts


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(
        detect_intent_texts(os.environ['PROJECT_ID'],
                            '12567231425634',
                            update.message.text, 'ru'))


def main():
    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          echo))
    updater.start_polling()


if __name__ == '__main__':
    main()
