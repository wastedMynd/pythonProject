from flask_restful import Resource
from Lottery.rest_flask_api.resource.game_info import GameInfo
from Lottery.rest_flask_api.scrapper.lotto_plus1.draw_scrapper import get_draw
from Lottery.rest_flask_api.scrapper.lotto_plus1.history_scrapper import get_history


class LottoPlus1(Resource):
    def get(self, function):
        if function == "info":
            return GameInfo.LOTTO_PLUS_1.value[0]
        elif function == "draw":
            return get_draw()
        elif function == "history":
            return get_history()
        else:
            return {f"{function}": dict(GameInfo.LOTTO_PLUS_1.value[0])[f"{function}"]}
