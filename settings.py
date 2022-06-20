from os import environ

SESSION_CONFIGS = [
    dict(
        name='woon_study',
        app_sequence=['s1_instructions', 's1_end'],
        num_demo_participants=10,
        use_browser_bots=False
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
    mturk_hit_settings=dict(
    keywords='bonus, study',
    title='survey-example',
    description='Description for your experiment',
    frame_height=500,
    template='global/mturk_template.html',
    minutes_allotted_per_assignment=60,
    expiration_hours=7 * 24,
    qualification_requirements=[]
    # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes
    )
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY =

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

#uncomment when ready to go to production (comment out when demoing)
environ['OTREE_ADMIN_PASSWORD'] = 'test' #password goes here
environ['OTREE_PRODUCTION'] = '1'
environ['OTREE_AUTH_LEVEL']='STUDY'

ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ROOMS = [
    dict(
        name='test',
        display_name='test',
    ),
]

PARTICIPANT_FIELDS = [
    'coin_toss_display'
]

SESSION_FIELDS = [
    'participant_parameters',
]
