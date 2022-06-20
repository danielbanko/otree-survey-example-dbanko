import csv
from otree.api import Currency as c, currency_range, expect, Bot, SubmissionMustFail
from s1_end import *
from random import randint

class PlayerBot(Bot):

    cases = [
        'success',  # players enter valid inputs
        # 'fail',  # players enter invalid inputs
    ]
    def play_round(self):
        # random.seed(10)

        class PlayerBot(Bot):
            cases = [
                'success',  # players enter valid inputs
                # 'fail',  # players enter invalid inputs
            ]

            def play_round(self):
                # start, each yield will be run "self.round_number" of times.
                player_list = self.subsession.get_players()
                case = self.case
                if case == 'success':
                    yield Thank