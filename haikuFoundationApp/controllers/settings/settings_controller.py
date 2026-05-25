class SettingsController:

    def get(self, event):
        return {
            "module": "SETTINGS",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "SETTINGS",
            "action": "POST"
        }
