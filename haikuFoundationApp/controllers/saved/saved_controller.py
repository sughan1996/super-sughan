from haikuFoundationApp.jobs.usersActivityHandler import get_users_saved_articles

class SavedController:
    def get(self, event):
        return {
            "module": "SAVED",
            "action": "GET"
        }

    def post(self, event):
        userId = event['body']['userId']
        resp = get_users_saved_articles(userId)
        return resp


