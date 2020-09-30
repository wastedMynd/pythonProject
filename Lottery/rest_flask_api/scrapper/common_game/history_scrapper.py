from Lottery.rest_flask_api.driver.chrome_driver import ChromeDriver
import re


def get_history(url) -> dict:
    # lotto history draw result.
    lotto_history_result_site = url

    chrome_driver = ChromeDriver()
    driver = chrome_driver.___setup_web_driver___()
    driver.get(lotto_history_result_site)

    # assert page's title; equals "Lotto Historical Result"
    page_title = ___get_page_title___(driver)

    # region columns, and draw history result list scrapping.
    #history_results = driver.find_element_by_id("lotto-results")
    #assert history_results is not None

    game_table1 = driver.find_element_by_class_name("gameTable1")
    assert game_table1 is not None

    # region columns scrapping.
    table_head = game_table1.find_element_by_class_name("tableHead")
    assert table_head is not None

    table_row = table_head.find_element_by_class_name("tableRow")
    assert table_row is not None

    columns = ___get_game_columns__(table_row)
    assert columns is not None and len(columns) > 0
    # endregion

    # region draw history result list scrapping.
    draw_history_result_list = ___get_history_draw_list___(game_table1, columns)
    assert draw_history_result_list is not None and len(draw_history_result_list) > 0
    # endregion
    # endregion

    if not chrome_driver.DEBUGGING:
        # terminate the browser window
        driver.quit()

    return {"draw_result_title": page_title, "draw_history_result_list": draw_history_result_list}


def ___get_page_title___(driver) -> str:
    return driver.title


def ___get_game_columns__(table_row) -> list:
    game_column = table_row.find_element_by_class_name("col1")
    assert game_column is not None

    game_date_column = table_row.find_element_by_class_name("col2")
    assert game_date_column is not None

    game_winning_numbers_column = table_row.find_element_by_class_name("col4")
    assert game_winning_numbers_column is not None

    game_column = 'DRAW ID'
    game_date_column = 'DRAW DATE'
    game_winning_numbers_column = 'DRAW WINNING NUMBERS'

    game_column = game_column.lower().replace(" ", "_")
    assert game_column is not None

    game_date_column = game_date_column.lower().replace(" ", "_")
    assert game_date_column is not None

    game_winning_numbers_column = game_winning_numbers_column.lower().replace(" ", "_")
    assert game_winning_numbers_column is not None

    return [game_column, game_date_column, game_winning_numbers_column]


def ___get_history_draw_entry___(table_row, columns) -> dict:
    # data_  = 'LOTTO\sDRAW\s2053\n2020-09-02\n09\n16\n21\n28\n37\n48\n+\n49'
    data = table_row.text

    # regex data, pattern for
    # id $1: \w+\s\w+\s(\d+)\n
    # date $2: (\d{4}[-]\d{2}[-]\d{2})\n
    # numbers $3: ((\d{2}\n)+)
    # bonus $5: [+]\n(\d{2})

    # pattern: \w+\s\w+\s(\d+)\n(\d{4}[-]\d{2}[-]\d{2})\n((\d{2}\n)+)[+]\n(\d{2})
    pattern = '(\\w+\\s+)+(\\d+)\n(\\d{4}[-]\\d{2}[-]\\d{2})\n((\\d{2}\n)+)[+]\n(\\d{2})'

    match = re.match(pattern, data)
    assert match is not None

    # draw_id_data
    draw_id_data = match.group(2)
    assert draw_id_data is not None

    # draw_date_data
    draw_date_data = match.group(3)
    assert draw_date_data is not None

    # draw_winning_numbers_data
    draw_winning_numbers_data = match.group(4)
    assert draw_winning_numbers_data is not None
    draw_winning_numbers_data = str(draw_winning_numbers_data.replace("\n", " ").strip())
    draw_winning_numbers_data = [int(number) for number in draw_winning_numbers_data.split(" ")]

    draw_winning_bonus_number_data = match.group(6)
    assert draw_winning_bonus_number_data is not None

    return {
        columns[0]: int(draw_id_data),
        columns[1]: str(draw_date_data),
        columns[2]: {
            'numbers': list(draw_winning_numbers_data),
            'bonus_number': int(draw_winning_bonus_number_data)
        }
    }


def ___get_history_draw_list___(game_table1, columns) -> list:
    table_body = game_table1.find_element_by_class_name("tableBody")
    assert table_body is not None

    table_rows = table_body.find_elements_by_class_name('tableRow')
    assert table_rows is not None

    return [___get_history_draw_entry___(table_row_, columns) for table_row_ in table_rows]
