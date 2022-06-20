import itertools
from otree.api import *
from fractions import Fraction
from itertools import cycle
import random, csv


doc = """
this app implements the s1_instructions for the survey and includes the comprehension checks as of February 2022. As of April 2022, it has been updated with the treatment logic.
"""


class Constants(BaseConstants):
    name_in_url = 's1_instructions'
    players_per_group = None
    temp = [] #used in response_choices function

    # list of payment mechanisms
    elicitation_mechanisms = ['flat', 'bdm', 'bsr']

    # build rounds for comprehension checks
    with open('s1_instructions/surveyqs_intro.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        round_parameters = []
        rounds_for_comprehension = 0
        for row in reader:
            rounds_for_comprehension += 1

    num_rounds = rounds_for_comprehension

    survey_dict={}



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    elicit_type = models.StringField(intial='NA')
    consent_form = models.IntegerField(   initial=-1,
                                          label="",
                                          widget=widgets.RadioSelect,
                                          choices=[
       [1, 'I have read the above and consent to take part in this study'],
       [2, 'I do not wish to participate'],
    ])

    gender = models.IntegerField(initial=-1, label="What is your gender?",widget=widgets.RadioSelect,choices=[
        [1, 'Male'],
        [2, 'Female'],
        [3, 'Other'],
    ])

    age = models.IntegerField(initial=-1, label="What is your age?",widget=widgets.RadioSelect,choices=[
        [1, 'Under 18'],
        [2, '18 - 24'],
        [3, '25 - 34'],
        [4, '35 - 44'],
        [5, '45 - 54'],
        [6, '55 - 64'],
        [7, '65 - 74'],
        [8, '75 - 84'],
        [9, '85 or older'],
    ])
    white = models.BooleanField(initial=0,blank=True)
    african_amer = models.BooleanField(initial=0,blank=True)
    hispanic = models.BooleanField(initial=0,blank=True)
    asian = models.BooleanField(initial=0,blank=True)
    native_amer = models.BooleanField(initial=0,blank=True)
    other = models.BooleanField(initial=0,blank=True)

    educ = models.IntegerField(initial=-1, label="What is the highest level of education you have completed?",widget=widgets.RadioSelect,choices=[
        [1, 'Less than High School'],
        [2, 'High School / GED'],
        [3, 'Some college'],
        [4, '2 year college degree (Associate)'],
        [5, '4 year college degree (Bachelor)'],
        [6, 'Post-graduate degree (Professional, Masters, Doctorate)'],
    ])

    subj_comprehension_1 = models.IntegerField(initial=-1,
                                          label="Did you find it easy or difficult to understand the instructions for determining the bonus?",
                                          widget=widgets.RadioSelect, choices=[
            [1, 'Extremely easy'],
            [2, 'Somewhat easy'],
            [3, 'Neither easy nor difficult'],
            [4, 'Somewhat difficult'],
            [5, 'Extremely difficult']
        ])

    subj_comprehension_2 = models.IntegerField(initial=-1,
                                          label="How simple or complex did you find the instructions for determining the bonus?",
                                          widget=widgets.RadioSelect, choices=[
            [1, 'Extremely simple'],
            [2, 'Somewhat simple'],
            [3, 'Neither simple nor complex'],
            [4, 'Somewhat complex'],
            [5, 'Extremely complex']
        ])


    attempted = models.IntegerField(initial=0)
    question_attempts = models.IntegerField(initial=0)
    question_label = models.StringField(initial="")
    question_id = models.StringField(initial="")
    response = models.IntegerField(initial=-1,widget=widgets.RadioSelect)
    response1 = models.IntegerField(initial=-1,widget=widgets.RadioSelect) #second attempt
    response2 = models.IntegerField(initial=-1,widget=widgets.RadioSelect) #third attemtpt
    choice_order = models.StringField(initial="")
    attempt = models.IntegerField(initial=0)
    correct_answer_index = models.IntegerField(initial=1)

#BUILT-IN METHODS
def creating_session(subsession):
    #RANDOMIZATION PROCEDURE
    # set elicitation mechanism in first round
    if subsession.round_number == 1:
        player_list = subsession.get_players()
        random.shuffle(player_list)
        elicitations = itertools.cycle(Constants.elicitation_mechanisms)
        print('entering randomization')
        for player in player_list:
            player.elicit_type = next(elicitations)
            participant = player.participant
            participant.elicit_type = player.elicit_type
            print(elicitations)

    #apply selected mechanism to player in all rounds
    for player in subsession.get_players():
        if subsession.round_number != 1:
            player_round1 = player.in_round(1)
            player.elicit_type = player_round1.elicit_type
            player.participant.vars['elicit_type'] = player.elicit_type

def check_slider_error_message(player, value):
    if value == 0 and player.round_number==1 and player.participant._is_bot==0:
        return 'Please click on the slider to select your belief.'

def belief_error_message(player,value):
    if player.round_number>1:
        if value == player.in_round(player.round_number - 1).belief and player.attempt == 0 and player.participant._is_bot==0:
            player.attempt = 1
            return 'Are you sure you want to enter the same belief as the previous round? Click next again if so.'

def response_choices(player):
    import csv
    import random
    if player.elicit_type == 'bdm':
        reader = csv.DictReader(open('s1_instructions/surveyqs_bdm.csv'))
    elif player.elicit_type == 'bsr':
        reader = csv.DictReader(open('s1_instructions/surveyqs_bsr.csv'))
    else:
        reader = csv.DictReader(open('s1_instructions/surveyqs_intro.csv'))
    Constants.survey_dict['q_id'] = []
    Constants.survey_dict['choices'] = []
    Constants.survey_dict['labels'] = []
    Constants.survey_dict['num_choices'] = []
    choices_list = []
    choice_order_list = []

    for row in reader:
        choices_dict = {}
        choices_per_question=[]
        label_per_question = []
        Constants.survey_dict['q_id'].append(row['q_id'])

        for i in range(0, int(row['num_choices'])):
            index = i + 1
            choices_dict.update({index: row['r' + str(index)]})
            choices_per_question.append([index, row['r' + str(index)]])

            label_per_question.append(row['q_label'])

        choices_list.append(choices_per_question)
        Constants.survey_dict['choices'].append(choices_dict)
        Constants.survey_dict['labels'].append(label_per_question)


    if player.attempted == 0:
        for i in range(0, Constants.num_rounds):
            if player.round_number == i + 1:
                cho = choices_list[i]
        Constants.survey_dict['temp'] = []
        Constants.survey_dict['temp'].append(random.sample(cho, len(cho)))
        Constants.survey_dict['temp'].append(Constants.survey_dict['temp'][0])
        Constants.survey_dict['temp'].append(Constants.survey_dict['temp'][0])
        player.attempted = player.attempted + 1

    choices = Constants.survey_dict['temp'][player.attempted-1]
    # print('choices is', choices)
    player.choice_order = ','.join(map(str, choices))
    choice_order_list.append(player.choice_order)
    # print('choice_order is', player.choice_order)
    index = 0
    for list in choices:
        if 1 in list:
            player.correct_answer_index = index
        index += 1
    # print('correct answer index in choice_order is:', player.correct_answer_index)
    player.question_label = Constants.survey_dict['labels'][player.round_number - 1][0]
    player.question_id = Constants.survey_dict['q_id'][player.round_number - 1]
    # print('question_id is', player.question_id)
    # print('round is:', player.round_number)
    return choices



def response_error_message(player, value):
    import csv
    if player.elicit_type == 'bdm':
        reader = csv.DictReader(open('s1_instructions/surveyqs_bdm.csv'))
    elif player.elicit_type == 'bsr':
        reader = csv.DictReader(open('s1_instructions/surveyqs_bsr.csv'))
    else:
        reader = csv.DictReader(open('s1_instructions/surveyqs_intro.csv'))

    Constants.survey_dict['error_message'] = []


    for row in reader:
        Constants.survey_dict['error_message'].append(row['error_message'])
    player.question_attempts = player.question_attempts + 1
    current_qid = str(Constants.survey_dict['q_id'][player.round_number - 1])
    # print(str(current_qid))
    if value != 1 and player.question_attempts == 1 and str(current_qid) not in ['numeracy_1','numeracy_2','numeracy_3','numeracy_4','numeracy_5','numeracy_6','numeracy_7','numeracy_8','numeracy_9'] and player.participant._is_bot==0:
        # print('entered')
        player.response1 = value
        return '<div style="background-color: #e0e0e0">Your answer is not correct. Please try again.<br></div>'
    if value != 1 and player.question_attempts > 1 and str(current_qid) not in ['numeracy_1','numeracy_2','numeracy_3','numeracy_4','numeracy_5','numeracy_6','numeracy_7','numeracy_8','numeracy_9'] and player.participant._is_bot==0:
        player.response2 = value
        return '<div style="background-color: #e0e0e0">Your answer is not correct. The correct answer is: ' + ' <br> <b> &emsp; &ensp;' + '"' + str(Constants.survey_dict['choices'][player.round_number-1][1]) + '" </b>' + '<br> Please select the correct answer from the options above to continue.</div>'





# PAGES
class Intro1(Page):
    form_model = 'player'
    form_fields = ['consent_form']

    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        print('upcoming_apps is', upcoming_apps)
        if player.consent_form == 2:
            return "s1_end"

class Intro2(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'white', 'african_amer', 'hispanic', 'asian', 'native_amer', 'other', 'educ']

    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        print('upcoming_apps is', upcoming_apps)
        if player.age == 1:
            return "s1_end"

class InstructionsA1(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class InstructionsA2(Page):
    def is_displayed(player):
        return player.round_number == 1

class InstructionsB1(Page):
    def is_displayed(player):
        return player.round_number == 9

class InstructionsB2(Page):
    def is_displayed(player):
        return player.round_number == 9

class InstructionsB3(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 9

class InstructionsB4(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 9

class InstructionsC1(Page):
    def is_displayed(player):
        return player.round_number == 13

class InstructionsD1(Page): #bdm
    @staticmethod
    def is_displayed(player):
        return player.round_number == 17 and player.elicit_type == 'bdm'

class InstructionsD1_(Page): #bsr
    @staticmethod
    def is_displayed(player):
        return player.round_number == 17 and player.elicit_type == 'bsr'



class InstructionsD1__(Page): #flat
    @staticmethod
    def is_displayed(player):
        return player.round_number == 17 and player.elicit_type == 'flat'

class InstructionsE1(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 17


class QuestionA(Page):
    form_model = 'player'
    form_fields = ['response']

    @staticmethod
    def vars_for_template(player):
        return dict(
            question_label=player.question_label
        )

class QuestionB(Page):
    form_model = 'player'
    form_fields = ['subj_comprehension_1', 'subj_comprehension_2']

    def is_displayed(player):
        return player.round_number == 17



page_sequence = [
    Intro1,
    Intro2,
    InstructionsA1,
    InstructionsA2,
    QuestionA,
    InstructionsB1,
    InstructionsB2,
    InstructionsB3,
    InstructionsB4,
    InstructionsC1,
    InstructionsD1,
    InstructionsD1_,
    InstructionsD1__,
    InstructionsE1,
    QuestionB
]