class MessagesController:

    def get(self, event):
        return {
            "module": "MESSAGES",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "MESSAGES",
            "action": "POST"
        }
