from flask_restful import Resource
from Lottery.rest_flask_api.resource.game_info import GameInfo
from Lottery.rest_flask_api.scrapper.lotto_plus2.draw_scrapper import get_draw
from Lottery.rest_flask_api.scrapper.lotto_plus2.history_scrapper import get_history


class LottoPlus2(Resource):
    def get(self, function) -> dict:
        if function == "info":
            return GameInfo.LOTTO_PLUS_2.value[0]
        elif function == "draw":
            return get_draw()
        elif function == "history":
            return get_history()
        else:
            return {f"{function}": dict(GameInfo.LOTTO_PLUS_2.value[0])[f"{function}"]}
