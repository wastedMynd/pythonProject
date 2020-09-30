from selenium import webdriver
import os
from Lottery.rest_flask_api.__init__ import Logging


class ChromeDriver:

    def __init__(self):
        base_path = "/home/sizwe/PycharmProjects/pythonProject"

        # download chrome driver https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/
        self.chromedriver_path = os.path.join(base_path, "Lottery/rest_flask_api/driver/chromedriver")

        self.DEBUGGING = False

    def ___setup_web_driver___(self) -> webdriver:
        # setup Chrome Options:
        setup_options = webdriver.ChromeOptions()

        # on Debugging mode; the chrome window is visible, otherwise it's not visible.
        setup_options.headless = not self.DEBUGGING

        # link webdriver to chromedriver_path and include setup_options
        return webdriver.Chrome(self.chromedriver_path, options=setup_options)
