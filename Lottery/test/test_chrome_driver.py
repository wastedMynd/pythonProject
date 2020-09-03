import unittest


class TestChromeDriver(unittest.TestCase):

    def setUp(self) -> None:
        from Lottery.rest_flask_api.chrome_driver import ___setup_web_driver___
        self.web_driver = ___setup_web_driver___()

    def test_setup_web_driver(self):
        # assert whether returns None, if so then the test, is a fail.
        self.assertIsNotNone(self.web_driver)
        pass

    def test_web_driver_get(self):
        # import the method to be tested...
        from Lottery.rest_flask_api.chrome_driver import web_driver_get

        # latest lotto draw result.
        lotto_latest_draw_result_site = "https://www.nationallottery.co.za/results/lotto"

        # assert whether the method returns a None, if so then the test, is a fail.
        self.assertIsNotNone(web_driver_get(lotto_latest_draw_result_site, self.web_driver))
        pass

    def tearDown(self) -> None:
        self.web_driver.quit()
