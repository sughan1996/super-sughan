class SavedController:
    def get(self, event):
        return {
            "module": "SAVED",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "SAVED",
            "action": "POST"
        }
