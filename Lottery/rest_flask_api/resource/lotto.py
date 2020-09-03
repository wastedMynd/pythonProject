from flask_restful import Resource
from Lottery.rest_flask_api.resource.game_info import GameInfo
from Lottery.rest_flask_api.scrapper.lotto.draw_scrapper import get_draw
from Lottery.rest_flask_api.scrapper.lotto.history_scrapper import get_history


class Lotto(Resource):
    def get(self, function):
        if function == "info":
            return GameInfo.LOTTO.value[0]
        elif function == "draw":
            return get_draw()
        elif function == "history":
            return get_history()
        else:
            return {f"{function}": dict(GameInfo.LOTTO.value[0])[f"{function}"]}
