import random

from haikuFoundationApp.dbmodels.staticDataController import EXPLORE_LIST_1, EXPLORE_LIST_2, EXPLORE_LIST_3, EXPLORE_LIST_4, \
    EXPLORE_LIST_5, \
    MANDATORY_LIST, ROMANTIC_LIST


class ExploreController:

    def get(self, event):
        return {
            "module": "EXPLORE",
            "action": "GET"
        }

    def post(self, event):
        TOTAL_LIST = (
                EXPLORE_LIST_1
                + EXPLORE_LIST_2
                + EXPLORE_LIST_3
                + EXPLORE_LIST_4
                + EXPLORE_LIST_5
        )
        first = random.choice(MANDATORY_LIST)
        second = random.choice(ROMANTIC_LIST)
        third = random.sample(TOTAL_LIST, 1)
        selected = third + [first] + [second]
        output = "\n\n".join(f"{haiku}" for haiku in selected)
        return output
