import time
import requests
import random
from bs4 import BeautifulSoup as webpage_parser

user_agent_list = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]

# Pick a random user agent
user_agent = random.choice(user_agent_list)

headers = {"User-Agent": user_agent,
           'Accept': 'text/html',
           'Accept-Language': 'en-US,en;q=0.5',
           'DNT': '1',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'
           }

def lotto():
    lotto_site = "https://www.nationallottery.co.za/results/lotto"

    print(f'{lotto_site} Web Scrapper!')

    source = requests.get(lotto_site, headers=headers)

    print(source)

    soup = webpage_parser(source.text, "lxml")

    draw_id = soup.find('div', class_='blockWrap resDetailView').find('div', class_='title')

    match = soup.find('div', class_='headerBox clearFix')

    innerHeaderBlock = match.find('div', class_="w50 fl").find('div', class_="innerHeaderBlock")

    titleHead = innerHeaderBlock.find('div', class_="titleHead")
    resultBalls = innerHeaderBlock.find('div', class_="resultBalls")
    date = innerHeaderBlock.find('div', class_="dateWrap").find("span", class_="date")

    print(f'{draw_id.text} {titleHead.text} date {date.text} : {resultBalls.text}')

    return draw_id, titleHead, date, resultBalls


def lotto_history_columns():
    lotto_site = "https://www.nationallottery.co.za/lotto-history"

    print(f'{lotto_site} Web Scrapper!')

    source = requests.get(lotto_site, headers=headers).text

    soup = webpage_parser(source, "lxml")

    tableRow = soup.find('div', class_='tableHead').find('div', class_='tableRow')

    col1 = tableRow.find('div', class_='col col1')
    gameDrawIDCol = col1.find('div', class_='inlineGroup').find('div', class_='labelName').text

    col2 = tableRow.find('div', class_='col col2')
    gameDateCol = col2.find('div', class_="labelName").text

    col3 = tableRow.find('div', class_='col col3')
    gameTypeCol = col3.find("div", class_="labelName").text

    col4 = tableRow.find('div', class_='col col4')
    gameWinningNumbersCol = col4.find("div", class_="labelName").text

    print(gameDrawIDCol, ",", gameDateCol, ",", gameTypeCol, ",", gameWinningNumbersCol)

    return gameDrawIDCol, gameDateCol, gameTypeCol, gameWinningNumbersCol

    # match = soup.find('div', class_='headerBox clearFix')


def lotto_history_row():
    lotto_site = "https://www.nationallottery.co.za/lotto-history"

    print(f'{lotto_site} Web Scrapper!')

    source = requests.get(lotto_site, headers=headers)

    soup = webpage_parser(source.content, "html5lib")

    time.sleep(2)

    tableBody = soup.find('div', class_='tableWrap')#.find('div', class_='tableBody')

    print(tableBody.prettify())

    # row_data = []
    # for tableRow in tableBody.findAll('div', class_='tableRow'):
    #   print(tableRow.prettify())

    pass


lotto_history_row()
