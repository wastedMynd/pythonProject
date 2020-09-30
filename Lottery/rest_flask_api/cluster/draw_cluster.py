import os
import json
from json import JSONDecodeError

from pymongo import MongoClient
import requests


def update_all_games_draw_result():
    games = ['lotto', 'lotto_plus1', 'lotto_plus2', 'powerball', 'powerball_plus', 'daily_lotto']

    response = list()

    for game in games:
        try:
            draw_cluster = DrawCluster(game)
            response.append(draw_cluster.update_draw_result())
        except JSONDecodeError:
            continue

    return response


class DrawCluster:

    def __init__(self, game):
        # get cluster connection and access properties
        DIR = "/home/sizwe/PycharmProjects/pythonProject/Lottery/rest_flask_api/cluster/"
        PROPERTIES_FILE = "cluster_properties.json"
        CLUSTER_PROPERTIES_PATH = os.path.join(DIR, PROPERTIES_FILE)

        with open(CLUSTER_PROPERTIES_PATH, "r") as properties_file:
            # read the file
            properties_file_reader = properties_file.read()

            # load file content to json Object
            content = json.loads(properties_file_reader)

            # extract individual content
            user = content["user"]
            password = content["password"]
            database = content["database"]

        CLUSTER_URL = f"mongodb+srv://{user}:{password}@nationallotteryzacluste.vffbf.mongodb.net/" + \
                      f"{database}?retryWrites=true&w=majority"

        # Online Cluster client connector
        cluster = MongoClient(CLUSTER_URL)

        self.database = cluster[database]

        self.collection = self.database[game]

        self.game = game

    def get_game_draw_url(self) -> str:
        return f"http://localhost:5000/{self.game}/draw"

    def update_draw_result(self):
        with requests.get(self.get_game_draw_url()) as response:
            response_json = response.json()

        online_draw_id = response_json["draw_id"]

        has_document = True

        try:
            cluster_draw = self.collection.find_one({"draw_id": online_draw_id})
            has_document = False if cluster_draw is None else cluster_draw["draw_id"] == online_draw_id
        finally:
            if has_document:
                return {
                    'game': self.game,
                    'draw_updated': False
                }

            self.collection.insert_one(response_json)

            return {
                'game': self.game,
                'draw_updated': True
            }


if __name__ == '__main__':
    print(update_all_games_draw_result())
