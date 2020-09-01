from flask_restful import Resource
from Lottery.rest_flask_api.lottery_games import LotteryGames
from Lottery.rest_flask_api.lotto_scapper import getLatestDrawResultInfo


class Lotto(Resource):
    def get(self, function):
        if function == "info":
            return LotteryGames.LOTTO.value[0]
        elif function == "draw":
            return getLatestDrawResultInfo()
        else:
            return {f"{function}": dict(LotteryGames.LOTTO.value[0])[f"{function}"]}
