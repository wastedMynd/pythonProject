import json
from Lottery.rest_flask_api.cluster.__init__ import get_cluster_url, get_cluster_properties
from Lottery.rest_flask_api.cluster.utils import get_game_draw_url
from pymongo import MongoClient
import requests


def update_all_games_draw_result() -> list:
    games = ["lotto", "lotto_plus1", "lotto_plus2", "powerball", "powerball_plus"]
    return [update_game_draw_result(game) for game in games]


def update_game_draw_result(game: str) -> dict:
    return DrawCluster(game).update_draw_result()


class DrawCluster:

    def __init__(self, game: str):

        cluster = MongoClient(get_cluster_url())

        properties = get_cluster_properties()

        self.database = cluster[properties.get("cluster")["database"]]

        self.collection = self.database[game]

        self.game = game

    def update_draw_result(self) -> dict:
        with requests.get(get_game_draw_url(self.game)) as response:
            response_json = response.json()

        key = "draw_id"

        online_draw_id = response_json[key]

        has_document = True

        try:
            cluster_draw = self.collection.find_one({key: online_draw_id})
            has_document = False if cluster_draw is None else cluster_draw[key] == online_draw_id
        finally:
            if has_document:
                return {
                    'game': self.game,
                    'updated': False,
                    'payload': response_json
                }

            self.collection.insert_one(response_json)

            return {
                'game': self.game,
                'updated': True,
                'payload': response_json
            }


if __name__ == '__main__':
    print(update_all_games_draw_result())
