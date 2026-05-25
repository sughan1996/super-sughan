class WriteController:
    def get(self, event):
        return {
            "module": "WRITE",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "WRITE",
            "action": "POST"
        }
