class FeaturedController:
    def get(self, event):
        return {
            "module": "FEATURED",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "FEATURED",
            "action": "POST"
        }
