# Utility For Movies Selection

## Description

Select movies from dataset. 
Dataset: https://grouplens.org/datasets/movielens/

## Usage

``python get-movies.py [-h] [-n] [-from] [-to] [-g]``

-h --help							show help message

-n --N [AMOUNT]						amount of output lines (default all lines)

-from  --year-from [YEAR]			lower year limit

-to  --year-to [YEAR]				upper year limit (default current year)

-g --genres [GENRES]				enum of genres (default any generes, format XXXX|XXXX)

## Examples

``python get-movies.py``

``python get-movies.py -n 5 -g "Action|Drama"``

``python get-movies.py -n 10 -r "live"``