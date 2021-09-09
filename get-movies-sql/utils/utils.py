import datetime

year_now = int(datetime.datetime.now().year)

DATA_FOLDER = 'data'
RATINGS_FILE = f'{DATA_FOLDER}/ratings.csv'
MOVIES_FILE = f'{DATA_FOLDER}/movies.csv'


YEAR_UNDEF = -1
RATING_UNDEF = -1
N_UNDEF = 'null'
REGEXP_UNDEF = '.*'
GENRES_UNDEF = 'null'
