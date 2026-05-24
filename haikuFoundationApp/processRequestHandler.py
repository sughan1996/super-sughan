from controllers.explore_controller import ExploreController
from controllers.home_controller import HomeController
from controllers.topics_controller import TopicController
from postController import post_profile_controller
from staticDataController import HAIKU_TYPES


AWS_REGION = "us-east-1"
COGNITO_USER_POOL_ID = "us-east-1_1pgqSzf45"
COGNITO_CLIENT_ID = "3q34c48o6fvaqbdmssvuovu86k"
JWKS_CACHE = {"jwks": None}


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

class MessagesController:

    def get(self, event):
        return {
            "module": "MESSAGES",
            "action": "GET"
        }

    def post(self, event):
        return {
            "module": "MESSAGES",
            "action": "POST"
        }

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

class ProfileController:

    def get(self, event):
        return {
            "module": "PROFILE",
            "action": "GET"
        }

    def post(self, event):
      return post_profile_controller(event)

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

class HaikuController:

  def get(self, event):
    return {
      "module": "HAIKU",
      "action": "GET"
    }

  def post(self, event):
    return {
      "module": "HAIKU",
      "action": "POST"
    }

class HaikuTypesController:

  def get(self, event):
    return {
      "module": "HAIKUTYPES",
      "action": "GET"
    }

  def post(self, event):
    return HAIKU_TYPES

class NotFoundController:

    def handle(self, event):
        return {
            "error": "Route not found"
        }

CONTROLLERS = {
    "/home": HomeController(),
    "/explore": ExploreController(),
    "/topics": TopicController(),
    "/saved": SavedController(),
    "/featured": FeaturedController(),
    "/write": WriteController(),
    "/profile": ProfileController(),
    "/trending": TrendingController(),
    "/haiku": HaikuController(),
    "/messages": MessagesController(),
    "/settings": SettingsController(),
    "/notifications": NotificationsController(),
    "/logout": LogoutController(),
}

FALLBACK = NotFoundController()



