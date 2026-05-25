class LogoutController:

    def get(self, event):
        return {
            "module": "LOGOUT",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "LOGOUT",
            "action": "POST"
        }
