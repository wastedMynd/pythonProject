from enum import Enum


class GameInfo(Enum):
    LOTTO = {
                "game_name": "lotto",
                "how_to_play": {
                    "quick_pick": "You can play the LOTTO game, by choosing a Quick Pick option;"
                                  "where the Lottery processing system randomly chooses 6 lucky numbers for you.",
                    "manual_pick": "You can manually choose your lucky numbers by following these easy steps.",
                    "manual_pick_steps": {
                        "step1": "Find a valid LOTTO Bet-slip.",
                        "step2": "Using a pen or pencil, choose 6 numbers from 1 to 52 numbers; "
                                 "on any board by marking your choice of numbers.",
                        "step3": "Take your Bet-slip to a teller at an "
                                 "approved Lottery retailer to make your payment.",
                        "step4": "You will receive a receipt from the teller with all your chosen numbers.",
                        "step5": "Make sure you write your name on the back of the receipt.",
                        "step6": "Look out for the next LOTTO Draw"
                                 " on SABC 2, Wed /Sat at 20h57 to see if you have won."
                    }
                },
                "number_picking_rules": {
                    "normal_numbers": {
                        "minimum_number": 1,
                        "maximum_number": 52,
                        "maximum_slots": 6
                    },
                    "extra_numbers": {
                        "minimum_number": 1,
                        "maximum_number": 52,
                        "maximum_slots": 1,
                        "is_bonus_picked": False,
                        "is_part_of_draw": True
                    }
                },
                "ticket_sales_close_time": "20h30",
                "draw_live_on": ["SABC 2"],
                "draw_date": ["Wed", "Sat"],
                "draw_time": "20h57",
                "payment": "R5.00",
                "player_reminder": {
                    "reminder1": "You can play as many boards as you want.",
                    "reminder2": "You can choose a Multi-Draw option, "
                                 "which allows you to play the same numbers over multiple draws.",
                    "reminder3": "A single LOTTO play will cost you R5.00 vat incl.",
                    "reminder4": "Ticket sales close at 8:30pm on any given draw day."
                },
                "latest_draw_result_url": "https://www.nationallottery.co.za/results/lotto",
                "draw_history_url": "https://www.nationallottery.co.za/lotto-history"
            },
    LOTTO_PLUS1 = {
                      "game_name": "lotto_plus1",
                      "how_to_play": {
                          "quick_pick": "You can play the LOTTO Plus 1 game"
                                        "by choosing a Quick Pick option where the Lottery processing system"
                                        "randomly chooses 6 lucky numbers for you.",
                          "manual_pick": "You can manually choose your lucky numbers by following these easy steps.",
                          "manual_pick_steps": {
                              "step1": "Find a valid LOTTO Bet-slip.",
                              "step2": "Using a pen / pencil, choose 6 numbers from 1 to 52 numbers"
                                       "on any board by marking your choice of numbers.",
                              "step3": "Take your Bet-slip to a teller at an approved "
                                       "Lottery retailer to make your payment.",
                              "step4": "You will receive a receipt from the teller with all your chosen numbers.",
                              "step5": "Make sure you write your name on the back of the receipt.",
                              "step6": "Look out for the next LOTTO Draw on SABC 2, "
                                       "Wed /Sat at 20h57 to see if you have won.",
                          }
                      },
                      "number_picking_rules": {
                          "normal_numbers": {
                              "minimum_number": 1,
                              "maximum_number": 52,
                              "maximum_slots": 6
                          },
                          "extra_numbers": {
                              "minimum_number": 1,
                              "maximum_number": 52,
                              "maximum_slots": 1,
                              "is_bonus_picked": False,
                              "is_part_of_draw": True
                          }
                      },
                      "ticket_sales_close_time": "20h30",
                      "draw_live_on": ["SABC 2"],
                      "draw_date": ["Wed", "Sat"],
                      "draw_time": "20h57",
                      "payment": "R7.50",
                      "player_reminder": {
                          "reminder1": "You can play as many boards as you want.",
                          "reminder2": "To play LOTTO PLUS 1, "
                                       "simply mark off the LOTTO PLUS 1 option on your Bet-slip.",
                          "reminder3": "In order to Play LOTTO PLUS 1, LOTTO has to be played.",
                          "reminder4": "You can choose a Multi-Draw option "
                                       "which allows you to play the same numbers over multiple draws.",
                          "reminder5": "A single LOTTO play will cost you R5.00 vat incl.",
                          "reminder6": "A single cost of LOTTO PLUS 1 will be R2.50 vat incl.",
                          "reminder7": "Ticket sales close at 8:30pm on any given draw day.",
                      },
                      "latest_draw_result_url": "https://www.nationallottery.co.za/results/lotto-plus-1-results",
                      "draw_history_url": "https://www.nationallottery.co.za/lotto-plus-1-history"
                  },
    LOTTO_PLUS2 = {
                      "game_name": "lotto_plus2",
                      "how_to_play": {
                          "quick_pick": "You can play the LOTTO Plus 2 games "
                                        "by choosing a Quick Pick option where the Lottery processing "
                                        "system randomly chooses 6 lucky numbers for you.",
                          "manual_pick": "You can manually choose your lucky numbers by following these easy steps.",
                          "manual_pick_steps": {
                              "step1": "Find a valid LOTTO Bet-slip.",
                              "step2": "Using a pen / pencil, choose 6 numbers from 1 to 52 numbers "
                                       "on any board by marking your choice of numbers.",
                              "step3": "Take your Bet-slip to a teller at an approved "
                                       "Lottery retailer to make your payment.",
                              "step4": "You will receive a receipt from the teller with all your chosen numbers.",
                              "step5": "Make sure you write your name on the back of the receipt.",
                              "step6": "Look out for the next LOTTO Draw on SABC 2, "
                                       "Wed /Sat at 20h57 to see if you have won.",
                          }
                      },
                      "number_picking_rules": {
                          "normal_numbers": {
                              "minimum_number": 1,
                              "maximum_number": 52,
                              "maximum_slots": 6
                          },
                          "extra_numbers": {
                              "minimum_number": 1,
                              "maximum_number": 52,
                              "maximum_slots": 1,
                              "is_bonus_picked": False,
                              "is_part_of_draw": True
                          }
                      },
                      "ticket_sales_close_time": "20h30",
                      "draw_live_on": ["SABC 2"],
                      "draw_date": ["Wed", "Sat"],
                      "draw_time": "20h57",
                      "payment": "R9.50",
                      "player_reminder": {
                          "reminder1": "You can play as many boards as you want.",
                          "reminder2": "To Play LOTTO PLUS 2, simply Mark LOTTO PLUS 2 option on your bet-slip.",
                          "reminder3": "In order to Play LOTTO PLUS 2, LOTTO and LOTTO PLUS 1 has to be played.",
                          "reminder4": "You can choose a Multi-Draw option "
                                       "which allows you to play the same numbers over multiple draws.",
                          "reminder5": "A single cost of LOTTO PLUS 2 will be R2.50 vat incl.",
                          "reminder6": "Ticket sales close at 8:30pm on any given draw day.",
                      },
                      "latest_draw_result_url": "https://www.nationallottery.co.za/results/lotto-plus-2-results",
                      "draw_history_url": "https://www.nationallottery.co.za/lotto-plus-2-history"
                  },
    DAILY_LOTTO = {
                      "game_name": "daily_lotto",
                      "how_to_play": {
                          "quick_pick": "You can play the DAILY LOTTO game "
                                        "by choosing a Quick Pick option where the lottery processing "
                                        "system randomly chooses 5 lucky numbers for you.",
                          "manual_pick": "You can manually choose your lucky numbers by following these easy steps.",
                          "manual_pick_steps": {
                              "step1": "Find a valid DAILY LOTTO Bet-slip.",
                              "step2": "Using a pen / pencil, choose 5 numbers from 1 to 36.",
                              "step3": "Take your Bet-slip to a teller at an approved Lottery "
                                       "retailer to make your payment.",
                              "step4": "You will receive a receipt from the teller with all your chosen numbers.",
                              "step5": "Make sure you write your name on the back of the receipt.",
                              "step6": "The games results are drawn every day at 21h00."
                                       "Results are available at retailers and online.",
                          }
                      },
                      "number_picking_rules": {
                          "normal_numbers": {
                              "minimum_number": 1,
                              "maximum_number": 36,
                              "maximum_slots": 5
                          },
                          "extra_numbers": {
                              "minimum_number": 1,
                              "maximum_number": 36,
                              "maximum_slots": 1,
                              "is_bonus_picked": False,
                              "is_part_of_draw": True
                          }
                      },
                      "ticket_sales_close_time": "20h30",
                      "draw_live_on": ["Retailers", "Online"],
                      "draw_date": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                      "draw_time": "21h00",
                      "payment": "R3.00",
                      "player_reminder": {
                          "reminder1": "You can play as many boards as you want.",
                          "reminder2": "You can choose a Multi-Draw option, "
                                       "which allows you to play the same numbers over multiple draws.",
                          "reminder3": "A single DAILY LOTTO play will cost you R3.00 VAT incl."
                      },
                      "latest_draw_result_url": "https://www.nationallottery.co.za/results/daily_lotto",
                      "draw_history_url": "https://www.nationallottery.co.za/daily-lotto-history"
                  },
    POWERBALL = {
                    "game_name": "powerball",
                    "how_to_play": {
                        "quick_pick": "You can play the PowerBall game by "
                                      "choosing a Quick Pick option where the Lottery processing system "
                                      "randomly chooses 6 lucky numbers for you.",
                        "manual_pick": "You can manually choose your lucky numbers by following these easy steps.",
                        "manual_pick_steps": {
                            "step1": "Find a valid POWERBALL Bet-slip.",
                            "step2": "Using a pen / pencil, choose 5 numbers from 1 to 50 "
                                     "and 1 extra number from 1 to 20.",
                            "step3": "Take your Bet-slip to a teller at "
                                     "an approved Lottery retailer to make your payment.",
                            "step4": "You will receive a receipt from the teller with all your chosen numbers.",
                            "step5": "Make sure you write your name on the back of the receipt.",
                            "step6": "Look out for the next PowerBall Draw "
                                     "on Mzansi Magic (channel 161)  and NewzRoom Afrika (channel 405),"
                                     "Tues/ Fri at 20h58 to see if you have won.",
                        }
                    },
                    "number_picking_rules": {
                        "normal_numbers": {
                            "minimum_number": 1,
                            "maximum_number": 50,
                            "maximum_slots": 5
                        },
                        "extra_numbers": {
                            "minimum_number": 1,
                            "maximum_number": 20,
                            "maximum_slots": 1,
                            "is_bonus_picked": True,
                            "is_part_of_draw": True
                        }
                    },
                    "ticket_sales_close_time": "20h30",
                    "draw_live_on": ["Mzansi Magic (channel 161)", "NewzRoom Afrika (channel 405)"],
                    "draw_date": ["Tue", "Fri"],
                    "draw_time": "20h58",
                    "payment": "R5.00",
                    "player_reminder": {
                        "reminder1": "You can play as many boards as you want.",
                        "reminder2": "You can choose a Multi-Draw option "
                                     "which allows you to play the same numbers over multiple draws.",
                        "reminder3": "A single PowerBall play will cost you R5.00 vat incl.",
                        "reminder4": "Ticket sales close at 8:30pm on any given draw day."
                    },
                    "latest_draw_result_url": "https://www.nationallottery.co.za/results/powerball",
                    "draw_history_url": "https://www.nationallottery.co.za/powerball-history"
                },
    POWERBALL_PLUS = {
        "game_name": "powerball_plus",
        "how_to_play": {
            "quick_pick": "You can play the PowerBall Plus game "
                          "by choosing a Quick Pick option where the Lottery processing system "
                          "randomly chooses 6 lucky numbers for you.",
            "manual_pick": "You can manually choose your lucky numbers by following these easy steps.",
            "manual_pick_steps": {
                "step1": "Find a valid POWERBALL Bet-slip.",
                "step2": "Using a pen / pencil, choose 5 numbers from 1 to 50 and 1 extra number from 1 to 20.",
                "step3": "Take your Bet-slip to a teller at an approved Lottery retailer to make your payment.",
                "step4": "You will receive a receipt from the teller with all your chosen numbers.",
                "step5": "Make sure you write your name on the back of the receipt.",
                "step6": "Look out for the next PowerBall Draw "
                         "on Mzansi Magic (channel 161)  and NewzRoom Afrika (channel 405),"
                         "Tues/ Fri at 20h58 to see if you have won.",
            }
        },
        "number_picking_rules": {
            "normal_numbers": {
                "minimum_number": 1,
                "maximum_number": 50,
                "maximum_slots": 5
            },
            "extra_numbers": {
                "minimum_number": 1,
                "maximum_number": 20,
                "maximum_slots": 1,
                "is_bonus_picked": True,
                "is_part_of_draw": True
            }
        },
        "ticket_sales_close_time": "20h30",
        "draw_live_on": ["Mzansi Magic (channel 161)", "NewzRoom Afrika (channel 405)"],
        "draw_date": ["Tue", "Fri"],
        "draw_time": "20h58",
        "payment": "R2.50",
        "player_reminder": {
            "reminder1": "You can play as many boards as you want.",
            "reminder2": "You can choose a Multi-Draw option "
                         "which allows you to play the same numbers over multiple draws.",
            "reminder3": "A single cost of PowerBall PLUS will be R2.50 vat incl.",
            "reminder4": "Ticket sales close at 8:30pm on any given draw day."
        },
        "latest_draw_result_url": "https://www.nationallottery.co.za/results/powerball-plus",
        "draw_history_url": "https://www.nationallottery.co.za/powerball-plus-history"
    }
