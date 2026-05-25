class TrendingController:

    def get(self, event):
        return {
            "module": "TRENDING",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "TRENDING",
            "action": "POST"
        }
