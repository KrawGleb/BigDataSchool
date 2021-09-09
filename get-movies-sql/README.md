# Utility For Movies Selection

## Description

Select movies from dataset. 
Dataset: https://grouplens.org/datasets/movielens/

## Usage

``get-movies.sh [--setupdb] [-h] [-n] [-from] [-to] [-g]``

-h --help							show help message

-n --N [AMOUNT]						amount of output lines (default all lines)

-from  --year-from [YEAR]			lower year limit

-to  --year-to [YEAR]				upper year limit (default current year)

-g --genres [GENRES]				enum of genres (default any generes, format XXXX|XXXX)

--setupdb							setup database before usage (downloads files, creates tables, views, procedures...)


## Examples

``python get-movies.py``

``python get-movies.py -n 5 -g "Action|Drama"``

``python get-movies.py -n 10 -r "live"``