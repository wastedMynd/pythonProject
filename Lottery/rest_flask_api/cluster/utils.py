import os
from Lottery.rest_flask_api.resource.game_info import GameInfo
from time import strftime
from Lottery.rest_flask_api.__init__ import Logging


@Logging
def get_draw_info_on(game_type) -> dict:
    draw_date = None
    draw_time = None
    is_game_type_found = False

    game_info = None
    for game in GameInfo:
        if game_type.lower() == game.name.lower():
            game_info = game.value[0]
            is_game_type_found = True
            break

    if is_game_type_found:
        draw_date = game_info["draw_date"]
        draw_time = game_info["draw_time"]

    return {
        "game_type": game_type,
        "draw_date": draw_date,
        "draw_time": draw_time,
        "is_game_type_found": is_game_type_found
    }


@Logging
def get_game_draw_url(game) -> str:
    return f"http://localhost:5000/{game}/draw"


@Logging
def get_draw_props_path(file) -> str:
    DIR = "/home/sizwe/PycharmProjects/pythonProject/Lottery/rest_flask_api/cluster/"
    return os.path.join(DIR, file)


@Logging
def get_draw_cluster_connection_url(user, password, database=""):
    CLUSTER_URL = f"mongodb+srv://{user}:{password}@nationallotteryzacluste.vffbf.mongodb.net/" + \
                  f"{database}?retryWrites=true&w=majority"
    return CLUSTER_URL


@Logging
def get_today_s_datetime_info() -> dict:
    # today_date format yyyy-mm-dd
    # today_weekday format in weekdays in this pattern "Mon,Tue,.."
    # today_time format 24hrs and in this pattern "20h30".
    return {
        "today_date": strftime("%Y-%m-%d"),
        "today_weekday": strftime("%a"),
        "today_time": strftime("%Hh%M")
    }
