import argparse
import re
import sys

import utils

strerr = sys.stderr

def select_movies(amount=-1, regexp='.*', year_from=utils.YEAR_UNDEF, year_to=utils.year_now, genres=''):
	"""
	Selects records matching parameters
	:param amount: amount of output lines (default all lines)
	:param regexp: regular expression for title (default any symbols)
	:param year_from: lower year limit (default=0)
	:param year_to: upper year limit (default current date)
	:param genres: enum of genres (default any generes, format XXXX|XXXX)
	:return: list of dictionaries. Dictionaries contains following data: id, title, year, genres, count of ratings,
	ratings sum and rating
	"""
	movies = []
	sample_genres = []
	try:
		with open(utils.MOVIES_FILE) as movies_file:
			next(movies_file)  # skip header
			for line in movies_file:
				movie_info = parse_csv_line(line.strip('\n'))
				if check_regexp(movie_info['title'], regexp) and \
					check_year(movie_info['year'], year_from, year_to) and \
					check_genres(movie_info['genres'], genres):
					movies.append(movie_info)

					for genre in movie_info['genres']:
						if genre not in sample_genres:
							sample_genres.append(genre)
	except FileNotFoundError as file_error:
		strerr.write(str(file_error))
		raise file_error

	define_ratings(movies)
	movies = sorted(movies, key=lambda movie: (-movie['rating'], -movie['year']))

	amount = len(movies) if amount == -1 else amount

	if not genres:
		display_grouped_by_genres(movies, sample_genres, amount)
	else:
		display_grouped_by_genres(movies, genres, amount)


def check_regexp(title, regexp):
	"""
	Checks the string by expression
	:param title: string with title
	:param regexp: string with regular expression
	:return: True if title contains any substrings match regexp, else False
	"""
	return bool(re.findall(regexp, title))


def check_year(year, year_from, year_to):
	"""
	Checks if the year is within the bounds [year_from; year_to]
	:param year: film release year
	:param year_from: lower year limit
	:param year_to: upper year limit
	:return: True if year is between year_from and year_to, else False
	"""
	return year_from <= year <= year_to


def check_genres(genres, target_genres):
	"""
	Checks if there are genres in target_genres
	:param genres: movie genres list
	:param target_genres: list of selected genres
	:return: True if target_genres and genres intersect, else False
	"""
	if not target_genres:
		return True

	for genre in genres:
		if genre in target_genres:
			return True

	return False


def define_ratings(movies):
	"""
	Reads the rating from RATINGS_FILE and writes it to the dictionary
	:param movies: list of movies
	"""
	try:
		with open(utils.RATINGS_FILE) as ratings_file:
			next(ratings_file)  # skip header
			for rating_line in ratings_file:
				rating_line = rating_line.split(',')
				add_rating(movies, int(rating_line[1]), float(rating_line[2]))
	except FileExistsError as file_error:
		strerr.write(str(file_error))
		raise file_error

	for movie in movies:
		if movie['ratingCount'] > 0:
			movie['rating'] = round(movie['ratingSum'] / movie['ratingCount'], 2)
		else:
			movie['rating'] = utils.RATING_UNDEF


def add_rating(movies, movie_id, rating):
	"""
	Looking for a movie and adding a rating to it
	:param movies: list of movies
	:param movie_id: target movie id
	:param rating: rating value
	"""
	start_index = 0
	end_index = len(movies) - 1
	mid_index = len(movies) // 2
	while movies[mid_index]['id'] != movie_id and start_index <= end_index:
		if movie_id > movies[mid_index]['id']:
			start_index = mid_index + 1
		else:
			end_index = mid_index - 1
		mid_index = (start_index + end_index) // 2

	if start_index < end_index:
		movies[mid_index]['ratingSum'] += rating
		movies[mid_index]['ratingCount'] += 1


def parse_csv_line(line):
	"""
	Splits csv file line and writes info in dictionary
	:param line: csv file line
	:return: dictionary with info about movie
	"""
	properties_list = line.split(',')

	if properties_list[1][0] == '"':  # if title contains ',' symbol
		for item in properties_list[2:-1]:
			properties_list[1] += ',' + item
		properties_list[1] = properties_list[1][1:-1]

	properties = {}
	properties['id'] = int(properties_list[0])
	properties['title'] = properties_list[1].strip(' ')

	year = re.findall('\d\d\d\d', properties['title'])  # lookup all 4-digits substrings
	if year:
		properties['title'] = properties['title'][0:-6].strip(' ')
		properties['year'] = int(year[-1])
	else:
		properties['year'] = utils.YEAR_UNDEF

	if ',' in properties['title']:
		properties['title'] = '"' + properties['title'] + '"'

	properties['genres'] = properties_list[-1].split('|')
	for index, genre in enumerate(properties['genres']):
		if genre == '(no genres listed)':
			properties['genres'][index] = ''

	properties['ratingSum'] = 0
	properties['ratingCount'] = 0
	properties['rating'] = 0

	return properties


def init_parser():
	"""
	Register command line arguments
	:return parser: command line arguments parser
	"""
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', '--N', default=-1, help='amount of output lines (default all lines)')
	parser.add_argument('-r', '--regexp', default='.*', help='regular expression for title (default any symbols)')
	parser.add_argument('-from', '--year-from', default=utils.YEAR_UNDEF, help='lower year limit')
	parser.add_argument('-to', '--year-to', default=utils.year_now,
	                    help='upper year limit (default current year)')
	parser.add_argument('-g', '--genres', default='', help='enum of genres (default any generes, format XXXX|XXXX)')

	return parser


def display_grouped_by_genres(movies, genres, amount):
	"""
	Groups data by genres and displays it to the console
	:param movies: list of movies
	:param genres: enum of genres
	:param amount: amount of output lines
	"""
	print('genre, title, year, rating')  # header
	for genre in genres:
		movies_count = 0
		for movie in movies:
			if genre in movie['genres'] and movies_count < amount:
				title = movie['title']
				year = movie['year'] if movie['year'] != utils.YEAR_UNDEF else ''
				rating = movie['rating'] if movie['rating'] != utils.RATING_UNDEF else ''
				print(f'{genre},{title},{year},{rating}')
				movies_count += 1


def main():
	args_parser = init_parser()
	namespace = args_parser.parse_args()
	amount = int(namespace.N)
	regexp = namespace.regexp
	year_from = int(namespace.year_from)
	year_to = int(namespace.year_to)

	genres = ''
	if namespace.genres:
		genres = namespace.genres[0]

	select_movies(amount=amount, regexp=regexp, year_from=year_from, year_to=year_to, genres=genres)


if __name__ == '__main__':
	main()
