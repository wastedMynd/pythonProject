from flask_restful import Resource
from Lottery.rest_flask_api.lottery_games import LotteryGames


class DailyLotto(Resource):
    def get(self, function): return LotteryGames.DAILY_LOTTO.value[0] if function == "info" else {
        f"{function}": dict(LotteryGames.DAILY_LOTTO.value[0])[f"{function}"]
    }