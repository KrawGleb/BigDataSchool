import argparse
from utils import utils
from admin.sql_connection import get_movies


def init_parser():
	"""
	Register command line arguments
	:return parser: command line arguments parser
	"""
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', '--N', default=utils.N_UNDEF, help='amount of output lines (default all lines)')
	parser.add_argument('-r', '--regexp', default=utils.REGEXP_UNDEF, help='regular expression for title (default any symbols)')
	parser.add_argument('-from', '--year-from', default=utils.YEAR_UNDEF, help='lower year limit')
	parser.add_argument('-to', '--year-to', default=utils.year_now,
	                    help='upper year limit (default current year)')
	parser.add_argument('-g', '--genres', default=utils.GENRES_UNDEF, help='enum of genres (default any generes, format XXXX|XXXX)')

	return parser


def main():
	parser = init_parser()
	namespace = parser.parse_args()

	n = namespace.N
	genres = namespace.genres
	regexp = namespace.regexp
	year_from = namespace.year_from
	year_to = namespace.year_to

	get_movies(n, year_from, year_to, regexp, genres)


if __name__ == '__main__':
	main()
