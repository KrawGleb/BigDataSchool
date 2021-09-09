"""
File parser
csv => parquet
parquet => csv
"""
import fastparquet as fsp
import pandas as pd
import argparse
import sys


def convert_csv_to_parq(source, destination, delimiter=',', decimal='.'):
	"""
	Convert csv format to parquet. New parquet file saves in destination directory.
	:param source: name of target file
	:param destination: name of converted file
	:param delimiter: string of length 1. Field delimiter for the input file. (default=',')
	:param decimal: character recognized as decimal  (default='.'). E.g. use ‘,’ for European data.
	"""
	stderr = sys.stderr
	try:
		pd.read_csv(source, delimiter=delimiter, decimal=decimal).to_parquet(destination)
	except FileNotFoundError as file_error:
		stderr.write(str(file_error) + '\n')
		raise file_error
	except MemoryError as memory_error:
		stderr.write(str(memory_error) + '\n')
		raise memory_error


def convert_parq_to_csv(source, destination, delimiter=',', decimal='.'):
	"""
	Convert parquet format to csv. New csv file saves in destination directory
	:param source: path to target file
	:param destination: name of converted file
	:param delimiter: string of length 1. Field delimiter for the output file. (default=',')
	:param decimal: character recognized as decimal  (default='.'). E.g. use ‘,’ for European data.
	"""
	stderr = sys.stderr
	try:
		file = fsp.ParquetFile(source)
		file.to_pandas().to_csv(destination, index=False, sep=delimiter, decimal=decimal)
	except FileNotFoundError as file_error:
		stderr.write(str(file_error) + '\n')
		raise file_error
	except MemoryError as memory_error:
		stderr.write(str(memory_error) + '\n')
		raise memory_error


def get_schema(path):
	"""
	Show parquet file schema
	:param path: path to file
	:return: return schema of parquet file
	"""
	stderr = sys.stderr
	try:
		file = fsp.ParquetFile(path)
	except FileNotFoundError as file_error:
		stderr.write(str(file_error) + '\n')
		raise file_error
	return file.schema


def init_parser():
	"""
	Register command line arguments
	:return parser: command line arguments parser
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-c2p', '--csv2parquet', nargs=2, help='convert csv file to parquet', metavar='FILENAME')
	parser.add_argument('-p2c', '--parquet2csv', nargs=2, help='convert parquet file to csv', metavar='FILENAME')
	parser.add_argument('-sh', '--get-schema', nargs=1, help='get parquet file schema', metavar='FILENAME')
	parser.add_argument('-d', '--delimiter', nargs=1, default=',', help='set new delimiter in csv file (default \',\'). Must be a 1-character string',
	                    metavar='DELIMITER')
	parser.add_argument('-dec', '--decimal', nargs=1, default='.',
	                    help='character recognized as decimal  (default \'.\'). E.g. use ‘,’ for European data. Must be a 1-character string',
	                    metavar='SEPARATOR')

	return parser


def main():
	args_parser = init_parser()
	namespace = args_parser.parse_args()

	if namespace.csv2parquet:
		source = namespace.csv2parquet[0]
		destination = namespace.csv2parquet[-1]
		delimiter = namespace.delimiter[0][0]  # delimiter must be a 1-character string
		decimal = namespace.decimal[0][0]      # decimal must be a 1-character string
		convert_csv_to_parq(source, destination, delimiter, decimal)

	elif namespace.parquet2csv:
		source = namespace.parquet2csv[0]
		destination = namespace.parquet2csv[-1]
		delimiter = namespace.delimiter[0]
		decimal = namespace.decimal[0]
		convert_parq_to_csv(source, destination, delimiter, decimal)

	elif namespace.get_schema:
		filename = namespace.get_schema
		print(get_schema(filename))


if __name__ == '__main__':
	main()
