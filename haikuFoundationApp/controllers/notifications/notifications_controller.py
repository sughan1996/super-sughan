class NotificationsController:

    def get(self, event):
        return {
            "module": "NOTIFICATIONS",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "NOTIFICATIONS",
            "action": "POST"
        }
