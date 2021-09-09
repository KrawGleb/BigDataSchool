from mysql.connector import MySQLConnection, Error, DataError
from configparser import ConfigParser

CONFIG_FILE = 'utils/config.ini'


def connect():
    """
    Connect to database
    :return: db connection
    """
    db_config = read_db_config()

    try:
        return MySQLConnection(**db_config)
    except Error as error:
        print(error)
    print('return None type')
    return None


def read_db_config(filepath=CONFIG_FILE, section='mysql'):
    """
    Read and parse db config
    :param filepath: config file path
    :param section: section with setups
    """
    parser = ConfigParser()
    parser.read(filepath)

    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filepath} file')

    return db_config


def get_movies(n, year_from, year_to, regexp, genres):
    conn = connect()
    cursor = conn.cursor()
    print('genre, title, year, rating')
    proc_query = f'CALL usp_find_top_rated_movies({n}, "{regexp}", {year_from}, {year_to}, ' + (f'"{genres})"' if genres != 'null' else f'{genres})')
    print(proc_query)
    result = cursor.execute(proc_query, multi=True)
    try:
        for cur in result:
            if cur.with_rows:
                for row in cur.fetchall():
                    print(*row)
    except:
        return
