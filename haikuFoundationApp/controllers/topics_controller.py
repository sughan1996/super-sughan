import random

from staticDataController import TOPICS_LIST


class TopicController:

    def get(self, event):
        output = TOPICS_LIST
        return ", ".join(f"{haiku}" for haiku in output)

    def post(self, event):
        if event.get('body').get('search'):
            search = event['body']['search']
            return ", ".join(f"{haiku}" for haiku in search)
        output = random.sample(TOPICS_LIST, 18)
        return ", ".join(f"{haiku}" for haiku in output)
