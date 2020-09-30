from Lottery.rest_flask_api.resource.game_info import GameInfo
import random
from Lottery.rest_flask_api.__init__ import Logging


@Logging
def getGameInfo(game) -> GameInfo:
    game_info = None

    for info in GameInfo:
        if str(game).lower() == str(info.name).lower():
            game_info = info
            break

    return game_info


@Logging
def get_quick_pick(game):
    if (game_info := getGameInfo(game)) is None:
        return None

    # region parse gameInfo
    number_picking_rules = game_info.value[0]["number_picking_rules"]

    normal_numbers = number_picking_rules["normal_numbers"]
    normal_numbers_minimum_number = normal_numbers["minimum_number"]
    normal_numbers_maximum_number = normal_numbers["maximum_number"]
    normal_numbers_maximum_slots = normal_numbers["maximum_slots"]

    extra_numbers = number_picking_rules['extra_numbers']
    extra_numbers_minimum_number = extra_numbers['minimum_number']
    extra_numbers_maximum_number = extra_numbers['maximum_number']
    extra_numbers_maximum_slots = extra_numbers['maximum_slots']

    # endregion

    @Logging
    def get_normal_numbers():
        numbers = []

        @Logging
        def get_generated_number():
            return random.randint(int(normal_numbers_minimum_number), int(normal_numbers_maximum_number))

        @Logging
        def is_number_in_range(generated_number):
            return int(normal_numbers_minimum_number) >= int(generated_number) <= int(normal_numbers_maximum_number)

        @Logging
        def is_number_repeating(generated_number):
            is_found = False
            for store_number in numbers:
                if generated_number == store_number:
                    is_found = True
                    break
            return is_found

        for _ in range(int(normal_numbers_maximum_slots)):
            number = get_generated_number()
            while not is_number_in_range(number) and is_number_repeating(number):
                number = get_generated_number()

            numbers.append(number)

        return numbers

    @Logging
    def get_extra_numbers(normal_numbers_):

        numbers = []

        @Logging
        def get_generated_number():
            return random.randint(int(extra_numbers_minimum_number), int(extra_numbers_maximum_number))

        @Logging
        def is_number_in_range(generated_number):
            return int(extra_numbers_minimum_number) >= int(generated_number) <= int(extra_numbers_maximum_number)

        @Logging
        def is_number_repeating(generated_number):
            is_found = False
            for store_number in numbers:
                if generated_number == store_number:
                    is_found = True
                    break
            return is_found

        @Logging
        def is_number_repeating_in_normal_numbers(generated_number):
            is_found = False
            for store_number in normal_numbers_:
                if generated_number == store_number:
                    is_found = True
                    break
            return is_found

        for _ in range(int(extra_numbers_maximum_slots)):
            number = get_generated_number()
            while not is_number_in_range(number) and is_number_repeating(number) and \
                    is_number_repeating_in_normal_numbers(number):
                number = get_generated_number()
            numbers.append(number)

        return numbers

    normal_numbers = get_normal_numbers()

    return {
        "game": game,
        "normal_numbers": normal_numbers,
        "extra_numbers": get_extra_numbers(normal_numbers)
    }


if __name__ == "__main__":
    get("common_game")
