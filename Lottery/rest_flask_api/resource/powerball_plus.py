from flask_restful import Resource
from Lottery.rest_flask_api.resource.game_info import GameInfo
from Lottery.rest_flask_api.scrapper.powerball_plus.draw_scrapper import get_draw
from Lottery.rest_flask_api.scrapper.powerball_plus.history_scrapper import get_history


class PowerBallPlus(Resource):
    def get(self, function):
        if function == "info":
            return GameInfo.POWER_BALL_PLUS.value[0]
        elif function == "draw":
            return get_draw()
        elif function == "history":
            return get_history()
        else:
            return {f"{function}": dict(GameInfo.POWER_BALL_PLUS.value[0])[f"{function}"]}
