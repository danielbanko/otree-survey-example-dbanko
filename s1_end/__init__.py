from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 's1_end'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Thank(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass





page_sequence = [Thank]
