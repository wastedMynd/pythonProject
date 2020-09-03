import unittest


class TestChromeDriver(unittest.TestCase):

    def setUp(self) -> None:
        from Lottery.rest_flask_api.driver.chrome_driver import ChromeDriver
        chrome_driver = ChromeDriver()
        self.web_driver = chrome_driver.___setup_web_driver___()

    def test_setup_web_driver(self):
        # assert whether returns None, if so then the test, is a fail.
        self.assertIsNotNone(self.web_driver)
        pass

    def test_web_driver_get(self):
        # latest lotto draw result.
        lotto_latest_draw_result_site = "https://www.nationallottery.co.za/results/lotto"

        # assert whether the method returns a None, if so then the test, is a fail.
        self.assertIsNotNone(self.web_driver.get(lotto_latest_draw_result_site))
        pass

    def tearDown(self) -> None:
        self.web_driver.quit()
