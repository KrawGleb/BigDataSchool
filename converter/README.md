# CSV/Parquet Converter

## Description

Simple file converter from csv to parquet format and from parquet to csv.

## Usage

``python converter.py [-h] [-c2p FILENAME FILENAME] [-p2c FILENAME FILENAME] [-sh FILENAME] [-d DELIMITER] [-dec SEPARATOR]``

-h --help                                                show help message

-c2p --csv2parquet [src-filename] [dst-filename]         convert csv file to parquet

-p2c --parquet2csv [src-filename] [dst-filename]         convert patquet file to csv

-sh --get-schema [file]                                  print parquet file schema

-d --delimiter [delimiter]                               change delimiter symbol in csv file (default ','). Must be a 1-character string

-dec -- decimal [separator]								 character recognized as decimal  (default '.'). E.g. use ‘,’ for European data. Must be a 1-character string


## Examples

There is a test file "names.csv" in the data folder.

``python converter.py -c2p "data/names.csv" "data/names.parq"``

``python converter.py -p2c "data/names.parq" "data/new_names.csv" -d "|"``

``python converter.py -p2c "data/names.parq" "data/new_names.csv" -d "|" -dec ","``