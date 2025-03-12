import random
from dotenv import load_dotenv
import os
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from intent import detect_intent_texts


def echo(event, vk_api, project_id):
    message, is_fallback = detect_intent_texts(f'vk-{project_id}', event.user_id, event.text, 'en')
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    project_id = os.environ['PROJECT_ID']
    vk_session = vk.VkApi(token=os.environ['VK_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, project_id)


if __name__ == "__main__":
    main()
