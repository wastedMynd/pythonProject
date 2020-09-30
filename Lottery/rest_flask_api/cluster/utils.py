import os
from Lottery.rest_flask_api.resource.game_info import GameInfo
from time import strftime


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


def get_storage_path(storage_file) -> str:
    return os.path.join("/home/sizwe/PycharmProjects/pythonProject/Lottery/rest_flask_api/storage/", storage_file)


def get_today_s_datetime_info() -> dict:
    # today_date format yyyy-mm-dd
    # today_weekday format in weekdays in this pattern "Mon,Tue,.."
    # today_time format 24hrs and in this pattern "20h30".
    return {
        "today_date": strftime("%Y-%m-%d"),
        "today_weekday": strftime("%a"),
        "today_time": strftime("%Hh%M")
    }
