from postController import post_home_controller


class HomeController:

    def get(self, event):
        return {
            "module": "HOME",
            "action": "GET"
        }

    def post(self, event):
        return post_home_controller(event)
