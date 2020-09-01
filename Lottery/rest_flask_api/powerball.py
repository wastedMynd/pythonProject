from flask_restful import Resource
from Lottery.rest_flask_api.lottery_games import LotteryGames


class PowerBall(Resource):
    def get(self, function): return LotteryGames.POWER_BALL.value[0] if function == "info" else {
        f"{function}": dict(LotteryGames.POWER_BALL.value[0])[f"{function}"]
    }