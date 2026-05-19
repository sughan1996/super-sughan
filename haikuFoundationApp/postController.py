from poemsHandler import get_poem_values
from usersHandler import get_user_id_values


def post_profile_controller(event):
  userId = event.get('body', {}).get('userId', None)
  resp = get_user_id_values(userId=userId)
  return resp


def post_home_controller(event):
  output = get_poem_values("homepage")
  return output
