from otree.api import Currency as c, currency_range, expect, Bot, SubmissionMustFail
from s1_instructions import *
from random import randint

# random.seed(10)

class PlayerBot(Bot):

    cases = [
        'success',  # players enter valid inputs
        # 'fail',  # players enter invalid inputs
    ]
    def play_round(self):
        # start, each yield will be run "self.round_number" of times.
        player_list = self.subsession.get_players()
        survey_dict = {}
        survey_dict['num_choices'] = []
        import csv
        if self.player.elicit_type == 'bdm':
            reader = csv.DictReader(open('s1_instructions/surveyqs_bdm.csv'))
        elif self.player.elicit_type == 'bsr':
            reader = csv.DictReader(open('s1_instructions/surveyqs_bsr.csv'))
        else:
            reader = csv.DictReader(open('s1_instructions/surveyqs_intro.csv'))
        for row in reader:
            survey_dict['num_choices'].append(int(row['num_choices']))
            print(survey_dict['num_choices'])


        case = self.case
        if case == 'success':
            if self.player.round_number == 1:
                yield Intro1, dict(consent_form=1)
                yield Intro2, dict(gender=randint(1, 3), age=randint(2, 9), white=randint(0, 1),
                                   african_amer=randint(0, 1), hispanic=randint(0, 1), asian=randint(0, 1),
                                   native_amer=randint(0, 1), other=randint(0, 1), educ=randint(1, 6))
                yield InstructionsA1,
                yield InstructionsA2,
            print('round_number is', self.player.round_number)
            print('num_choices is',survey_dict['num_choices'][self.player.round_number - 1])
            print('correct_answer_index is',self.player.correct_answer_index + 1)
            yield Submission(QuestionA,dict(response=randint(1,survey_dict['num_choices'][self.player.round_number-1]),response1=randint(1,survey_dict['num_choices'][self.player.round_number-1]),response2=self.player.correct_answer_index+1),check_html=False)
            if self.player.round_number == 9:
                yield InstructionsB1,
                yield InstructionsB2,
                yield InstructionsB3,
                yield InstructionsB4,
            if self.player.round_number == 13:
                yield InstructionsC1
            if self.player.round_number == 17:
                if self.player.elicit_type == 'bdm':
                    yield InstructionsD1
                elif self.player.elicit_type == 'bsr':
                    yield InstructionsD1_
                else:
                    yield InstructionsD1__
                yield InstructionsE1,
                yield QuestionB,dict(subj_comprehension_1=randint(1,5),subj_comprehension_2=randint(1,5))
