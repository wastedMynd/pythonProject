from enum import Enum


class GameType(Enum):
    LOTTO = 0
    LOTTO_PLUS = 1
    POWER_BALL = 2
    POWER_BALL_PLUS = 3


class GameRules:
    def __init__(self, game_type):
        self.set_game_type(game_type)
        pass

    def set_game_type(self, game_type):
        self.game_type = game_type
        if game_type == GameType.LOTTO:
            self.max_number = 49
        elif game_type == GameType.LOTTO_PLUS:
            self.max_number = 28
        elif game_type == GameType.POWER_BALL:
            self.max_number = 52
        if game_type == GameType.POWER_BALL_PLUS:
            self.max_number = 47
        pass

    def get_game_type(self):
        return self.game_type

    def get_max_number(self):
        return self.max_number


class Number:

    def __init__(self, number, game_type):
        self.game_rules = GameRules(game_type)
        self.set_number(number)

    def set_number(self, number):
        if number <= self.game_rules.get_max_number():
            self.number = number
        pass

    def get_number(self):
        return self.number

    def toString(self):
        return f"{self.game_rules.get_game_type()} luckyNumber {self.get_number()} of {self.game_rules.get_max_number()} "

luckyNumber = Number(15, GameType.LOTTO)
print(luckyNumber.toString())
