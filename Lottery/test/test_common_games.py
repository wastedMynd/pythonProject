import unittest
from unittest import TestCase
import requests
from Lottery.rest_flask_api.server import start_server


class TestCommonGames(TestCase):

    def setUp(self):
        start_server()
        self.request_url = "http://localhost:5000/{}/{}"
        self.games = [
            'lotto',
            'lotto_plus1',
            'lotto_plus2',
            'powerball',
            'powerball_plus',
        ]
        pass

    def test_common_game_request_info(self):
        for game in self.games:
            with requests.get(self.request_url.format(game, "info")) as response:
                self.assertTrue(response.ok)
                self.assertIsNotNone(response.json())

    def test_common_game_request_draw(self):
        for game in self.games:
            with requests.get(self.request_url.format(game, "draw")) as response:
                self.assertTrue(response.ok)
                self.assertIsNotNone(response.json())

    def test_common_game_request_history(self):
        for game in self.games:
            with requests.get(self.request_url.format(game, "history")) as response:
                self.assertTrue(response.ok)
                self.assertIsNotNone(response.json())

    def test_common_game_request_draw_update(self):
        for game in self.games:
            with requests.get(self.request_url.format(game, "draw_update")) as response:
                self.assertTrue(response.ok)
                self.assertIsNotNone(response.json())

    def test_common_game_request_quick_pick(self):
        for game in self.games:
            with requests.get(self.request_url.format(game, "quick_pick")) as response:
                self.assertTrue(response.ok)
                self.assertIsNotNone(response.json())

    def test_common_game_request_all_draw_update(self):
        with requests.get(self.request_url.format("all", "draw_update")) as response:
            self.assertTrue(response.ok)
            self.assertIsNotNone(response.json())


if __name__ == '__main__':
    unittest.main()
