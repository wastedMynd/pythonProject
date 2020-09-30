from Lottery.rest_flask_api.driver.chrome_driver import ChromeDriver
import re


def get_draw(url):
    # latest lotto draw result.
    lotto_latest_draw_result_site = url

    chrome_driver = ChromeDriver()
    driver = chrome_driver.___setup_web_driver___()
    driver.get(lotto_latest_draw_result_site)

    # assert page's title; equals "Ithuba National Lottery | Lotto Result"
    page_title = ___get_page_title___(driver)

    resDetailView = driver.find_element_by_class_name("resDetailView")

    # region draw id scrapping
    draw_id = ___get_draw_id___(resDetailView)
    # endregion

    # region draw results; balls, bonus ball, and date scrapping
    # region innerHeaderBlock holds; draw_result_balls, draw_result_bonus_ball, and draw date
    innerHeaderBlock = resDetailView.find_element_by_class_name("innerHeaderBlock")
    draw_result_balls, draw_result_bonus_ball = ___get_draw_result_balls_and_bonus___(innerHeaderBlock)
    draw_date = ___get_draw_date___(innerHeaderBlock)
    # endregion
    # endregion

    # region draw division scrapping
    gameTable2 = resDetailView.find_element_by_class_name("gameTable2")
    result_division_list = ___get_result_division_list___(gameTable2)
    # endregion

    # region draw result rollover info scrapping
    resMoreView = driver.find_element_by_class_name("resMoreView")
    draw_result_rollover_list = ___get_draw_result_rollover_list___(resMoreView)
    # endregion

    if not chrome_driver.DEBUGGING:
        # terminate the browser window
        driver.quit()

    return {
        "draw_result_title": str(page_title),
        "draw_id": int(draw_id),
        "draw_date": str(draw_date),
        "draw_winning_numbers": {
            "numbers": list(draw_result_balls),
            "bonus_number": int(draw_result_bonus_ball)
        },
        "draw_division_info": list(result_division_list),
        "draw_rollover_info": list(draw_result_rollover_list)
    }


def ___get_page_title___(driver) -> str:
    return driver.title


def ___get_draw_id___(res_detail_view) -> int:
    resDetailView_title_match = \
        re.match("(\\w+\\s)+(\\d+)", res_detail_view.find_element_by_class_name("title").text)
    assert resDetailView_title_match is not None

    # get draw id from resDetailView_title_match group 1
    return int(resDetailView_title_match.group(2))


def ___get_draw_result_balls_and_bonus___(inner_header_block) -> tuple:
    resultBalls = inner_header_block.find_element_by_class_name("resultBalls")
    assert resultBalls.text is not None

    result_ball_set = str(resultBalls.text).replace("\n", " ")

    draw_result_balls = result_ball_set.split(" + ")[0].strip()
    draw_result_balls = [int(number) for number in draw_result_balls.split(" ")]
    assert draw_result_balls is not None and len(draw_result_balls) > 0

    draw_result_bonus_ball = result_ball_set.split(" + ")[1].strip()

    return list(draw_result_balls), int(draw_result_bonus_ball)


def ___get_draw_date___(inner_header_block) -> str:
    dateWrap = inner_header_block.find_element_by_class_name("dateWrap")
    # assert dateWrap equals regex pattern "DRAW DATE: \d{4}-\d{2}-{2}"
    dateWrapMatch = re.match("DRAW DATE: (\\d{4}-\\d{2}-\\d{2})", dateWrap.text)
    assert dateWrapMatch is not None
    draw_date = dateWrapMatch.group(1)
    return draw_date


def ___get_result_division_list___(game_table_2) -> list:
    # region gameTable2 holds; column headers: divisions, winners and winnings
    tableHead = game_table_2.find_element_by_class_name("tableHead")
    tableRow = tableHead.find_element_by_class_name("tableRow")

    division_column_ = tableRow.find_element_by_class_name("col1")
    winners_column_ = tableRow.find_element_by_class_name("col2")
    winnings_column_ = tableRow.find_element_by_class_name("col3")

    division_column = str(division_column_.text).lower()
    winners_column = str(winners_column_.text).lower()
    winnings_column = str(winnings_column_.text).lower()
    # endregion

    # region tableBody holds; data for column headers: divisions, winners and winnings
    tableBody = game_table_2.find_element_by_class_name("tableBody")
    table_rows = tableBody.find_elements_by_class_name("tableRow")

    def get_result_division(table_row_data):
        division_data = table_row_data.find_element_by_class_name("col1")
        winners_data = table_row_data.find_element_by_class_name("col2")
        winnings_data = table_row_data.find_element_by_class_name("col3")

        division = division_data.text.replace("\n", " ")
        winners = winners_data.text.replace("\n", " ")
        winnings = winnings_data.text.replace("\n", " ")

        data_dictionary = {division_column: division, winners_column: winners, winnings_column: winnings}
        return data_dictionary

    return [get_result_division(table_row_data) for table_row_data in table_rows]


def ___get_draw_result_rollover_list___(res_more_view) -> list:
    tableBody = res_more_view.find_element_by_class_name("tableBody")
    table_rows = tableBody.find_elements_by_class_name("tableRow")

    def get_draw_result_rollover(table_row_data):
        column = table_row_data.find_element_by_class_name("col1")
        column = str(column.text).lower().strip().replace(" ", "_")
        column_data = table_row_data.find_element_by_class_name("col2")
        return {column: column_data.text}

    return [get_draw_result_rollover(table_row_data) for table_row_data in table_rows]
