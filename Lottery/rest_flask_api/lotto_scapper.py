from selenium import webdriver
import re

DEBUGING = False

def getLatestDrawResultInfo():

    # download chrome driver https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/
    path_to_chromedriver = "/home/sizwe/PycharmProjects/pythonProject/Lottery/rest_flask_api/chromedriver"

    # link webdriver to chromedriver
    opts = webdriver.ChromeOptions()
    opts.headless = not DEBUGING
    driver = webdriver.Chrome(path_to_chromedriver, options=opts)

    # latest lotto draw result.
    lotto_latest_draw_result_site = "https://www.nationallottery.co.za/results/lotto"

    # get the page, to the latest lotto draw result.
    driver.get(lotto_latest_draw_result_site)

    # assert page's title; equals "Ithuba National Lottery | Lotto Result"
    page_title = driver.title
    assert page_title == "Ithuba National Lottery | Lotto Result"

    # draw info holder [resDetailView]
    resDetailView = driver.find_element_by_class_name("resDetailView")

    # region draw id scrapping
    # region assert resDetailView.title, equals "LOTTO RESULTS FOR DRAW ID \d+"
    resDetailView_title_match = \
        re.match("LOTTO RESULTS FOR DRAW ID (\d+)", resDetailView.find_element_by_class_name("title").text)
    assert resDetailView_title_match is not None

    # get draw id from resDetailView_title_match group 1
    draw_id = int(resDetailView_title_match.group(1))
    # endregion
    # endregion

    # region draw results; balls, bonus ball, and date scrapping
    # region innerHeaderBlock holds; draw_result_balls, draw_result_bonus_ball, and draw date
    innerHeaderBlock = resDetailView.find_element_by_class_name("innerHeaderBlock")
    resultBalls = innerHeaderBlock.find_element_by_class_name("resultBalls")
    assert resultBalls.text is not None

    result_ball_set = str(resultBalls.text).replace("\n", " ")
    draw_result_balls = result_ball_set.split(" + ")[0].strip()
    draw_result_bonus_ball = result_ball_set.split(" + ")[1].strip()
    # endregion

    # region draw date holder, is dateWrap = "DRAW DATE: 2020-08-29"
    dateWrap = innerHeaderBlock.find_element_by_class_name("dateWrap")
    # assert dateWrap equals regex pattern "DRAW DATE: \d{4}-\d{2}-{2}"
    dateWrapMatch = re.match("DRAW DATE: (\d{4}-\d{2}-\d{2})", dateWrap.text)
    assert dateWrapMatch is not None
    draw_date = dateWrapMatch.group(1)
    # endregion
    # endregion

    # region draw division scrapping
    gameTable2 = resDetailView.find_element_by_class_name("gameTable2")
    # region gameTable2 holds; column headers: divisions, winners and winnings
    tableHead = gameTable2.find_element_by_class_name("tableHead")
    tableRow = tableHead.find_element_by_class_name("tableRow")

    division_column_ = tableRow.find_element_by_class_name("col1")
    winners_column_ = tableRow.find_element_by_class_name("col2")
    winnings_column_ = tableRow.find_element_by_class_name("col3")

    division_column = str(division_column_.text).lower()
    winners_column = str(winners_column_.text).lower()
    winnings_column = str(winnings_column_.text).lower()
    # endregion

    # region tableBody holds; data for column headers: divisions, winners and winnings
    tableBody = gameTable2.find_element_by_class_name("tableBody")
    tableRows = tableBody.find_elements_by_class_name("tableRow")

    result_division_list = []
    for tableRow_data in tableRows:
        division_data = tableRow_data.find_element_by_class_name("col1")
        winners_data = tableRow_data.find_element_by_class_name("col2")
        winnings_data = tableRow_data.find_element_by_class_name("col3")

        division = division_data.text.replace("\n", " ")
        winners = winners_data.text.replace("\n", " ")
        winnings = winnings_data.text.replace("\n", " ")

        data_dictionary = {division_column: division, winners_column: winners, winnings_column: winnings}
        result_division_list.append(data_dictionary)
    # endregion
    # endregion

    # region draw result rollover info
    draw_result_rollover_list = []
    resMoreView = driver.find_element_by_class_name("resMoreView")
    tableBody = resMoreView.find_element_by_class_name("tableBody")
    tableRows = tableBody.find_elements_by_class_name("tableRow")
    for tableRow_data in tableRows:
        column = tableRow_data.find_element_by_class_name("col1")
        column = str(column.text).lower().strip().replace(" ", "_")
        column_data = tableRow_data.find_element_by_class_name("col2")
        draw_result_rollover_list.append({column: column_data.text})

    # endregion

    if not DEBUGING:
        # terminate the browser window
        driver.quit()

    data = {"draw_result_title": page_title,
            "draw_result_id": draw_id,
            "draw_result_date": draw_date,
            "draw_result_numbers": {
                "balls": draw_result_balls,
                "bonus_ball": draw_result_bonus_ball
            },
            "draw_result_division_info": result_division_list,
            "draw_result_rollover_info": draw_result_rollover_list
            }

    return data


