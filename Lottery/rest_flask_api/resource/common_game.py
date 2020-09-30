from flask_restful import Resource
from Lottery.rest_flask_api.scrapper.lotto.draw_scrapper import get_draw as get_draw_online
from Lottery.rest_flask_api.resource.quickpick import get_quick_pick
from Lottery.rest_flask_api.scrapper.lotto.history_scrapper import get_history
from Lottery.rest_flask_api.cluster.draw_cluster import update_game_draw_result

from Lottery.rest_flask_api.resource.game_info import GameInfo


class CommonGameResources(Resource):
    def get(self, game_name, function="info") -> dict:

        game_info = GameInfo.LOTTO

        for this_game in GameInfo:
            try:
                if this_game.value[0]['game_name'] == game_name:
                    game_info = this_game
                    break
            except KeyError:
                if this_game.value['game_name'] == game_name:
                    game_info = this_game
                    break

        if function == "info":
            try:
                return game_info.value[0]
            except KeyError:
                return game_info.value
        elif function == "draw":
            try:
                return get_draw_online(game_info.value[0]["latest_draw_result_url"])
            except KeyError:
                return get_draw_online(game_info.value["latest_draw_result_url"])
        elif function == "draw_update":
            return update_game_draw_result(game_name)
        elif function == "history":
            try:
                return get_history(game_info.value[0]["draw_history_url"])
            except KeyError:
                return get_history(game_info.value["draw_history_url"])
        elif function == "quick_pick":
            return get_quick_pick(game_name)
        else:
            try:
                return {function: dict(game_info.value[0])[function]}
            except KeyError:
                return {function: dict(game_info.value)[function]}
