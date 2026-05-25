from haikuFoundationApp.requester.postController import post_profile_controller


class ProfileController:

    def get(self, event):
        return {
            "module": "PROFILE",
            "action": "GET"
        }

    def post(self, event):
        return post_profile_controller(event)
