from flask_restful import Resource
from Lottery.rest_flask_api.resource.game_info import GameInfo
from Lottery.rest_flask_api.scrapper.common_game.draw_scrapper import get_draw as get_draw_online
from Lottery.rest_flask_api.resource.quickpick import get_quick_pick
from Lottery.rest_flask_api.scrapper.common_game.history_scrapper import get_history

from Lottery.rest_flask_api.cluster.draw_cluster import update_game_draw_result

game_info = GameInfo.DAILY_LOTTO
game = game_info.value[0]['game_name']
latest_draw_result_url = "https://www.nationallottery.co.za/results/daily_lotto"
draw_history_url = "https://www.nationallottery.co.za/daily-lotto-history"


class DailyLotto(Resource):
    def get(self, function):
        if function == "info":
            return game_info.value[0]
        elif function == "draw":
            return get_draw_online(latest_draw_result_url)
        elif function == "draw_update":
            return update_game_draw_result(game)
        elif function == "history":
            return get_history(draw_history_url)
        elif function == "quick_pick":
            return get_quick_pick(game)
        else:
            return {function: dict(game_info.value[0])[function]}
