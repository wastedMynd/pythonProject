from selenium import webdriver

DEBUGGING = False


def ___setup_web_driver___() -> webdriver:
    # setup Chrome Options:
    setup_options = webdriver.ChromeOptions()

    # on Debugging mode; the chrome window is visible, otherwise it's not visible.
    setup_options.headless = not DEBUGGING

    # download chrome driver https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/
    chromedriver_path = "/home/sizwe/PycharmProjects/pythonProject/Lottery/rest_flask_api/chromedriver"

    # link webdriver to chromedriver_path and include setup_options
    web_driver = webdriver.Chrome(chromedriver_path, options=setup_options)

    return web_driver


def web_driver_get(url, web_driver=___setup_web_driver___()) -> webdriver:
    # get the page of url
    web_driver.get(url=url)

    return web_driver
