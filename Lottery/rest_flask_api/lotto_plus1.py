from flask_restful import Resource
from Lottery.rest_flask_api.lottery_games import LotteryGames


class LottoPlus1(Resource):
    def get(self, function): return LotteryGames.LOTTO_PLUS_1.value[0] if function == "info" else {
        f"{function}": dict(LotteryGames.LOTTO_PLUS_1.value[0])[f"{function}"]
    }