from dotenv import load_dotenv
import os
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    return response.query_result.fulfillment_text


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
