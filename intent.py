from dotenv import load_dotenv
import os
import requests
import json
from google.cloud import dialogflow


def load_questions(dir_name, filename):
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def upload_phrases(dir_name, filename, project_id):
    with open(os.path.join(dir_name, f'{filename}.json'), "r", encoding='utf-8') as file:
        phrases_json = file.read()

    phrases = json.loads(phrases_json)
    for phrase, questions in phrases.items():
        create_intent(project_id, phrase, questions['questions'], [questions['answer']])


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text, \
        response.query_result.intent.is_fallback


def main():
    load_dotenv()
    project_id = os.environ['PROJECT_ID']
    dir_name = 'files'
    filename = 'question'
    response_json = load_questions(dir_name, filename)
    os.makedirs(dir_name, exist_ok=True)
    with open(os.path.join(dir_name, f'{filename}.json'), 'w', encoding='utf-8') as file:
        json.dump(response_json, file, ensure_ascii=False)
    upload_phrases(dir_name, filename, project_id)


if __name__ == '__main__':
    main()
