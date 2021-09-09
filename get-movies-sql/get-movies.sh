#!/bin/bash

TABLES_DIR="admin/SQL/DDL/Tables"
PROCEDURES_DIR="admin/SQL/DDL/Procedures"
VIEWS_DIR="admin/SQL/DDL/Views"
LOAD_DATA_DIR="admin/SQL/DML/Populate tables scripts"
DATA_DIR="admin/data"

cur_dataset="ml-latest-small"
password="12345678"
user="root"

function download_and_unzip_data() {
  wget -O /tmp/source.zip -P /tmp "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
  unzip /tmp/source.zip -d /tmp
  rm /tmp/source.zip

  mv /tmp/$cur_dataset/movies.csv $DATA_DIR
  mv /tmp/$cur_dataset/ratings.csv $DATA_DIR

  rm -r /tmp/$cur_dataset
}

function setup_db() {
  function create_tables() {
    for file in $TABLES_DIR/*; do
      if [ "${file: -4}" == ".sql" ]; then
        mysql --local-infile --user="$user" --password="$password" <$file
      fi
    done
  }

  function create_procedures() {
    for file in $PROCEDURES_DIR/*; do
      if [ "${file: -4}" == ".sql" ]; then
        mysql --local-infile --user="$user" --password="$password" <$file
      fi
    done
  }

  function create_views() {
    for file in $VIEWS_DIR/*; do
      if [ "${file: -4}" == ".sql" ]; then
        mysql --local-infile --user="$user" --password="$password" <$file
      fi
    done
  }

  function load_data() {
    for file in "$LOAD_DATA_DIR"/*; do
      if [ "${file: -4}" == ".sql" ]; then
        mysql --local-infile --user="$user" --password="$password" <"$file"
      fi
    done
  }

  download_and_unzip_data
  create_tables
  create_procedures
  create_views
  load_data
  mysql --local-infile --user="$user" --password="$password" -vve "USE csv_files; CALL usp_fill_result_table"
}


while [ -n "$1" ]; do
  case "$1" in
  --help | -h)
    python3 get-movies.py -h
    break
    ;;
  --setupdb)
    setup_db
    shift
    ;;
  --N | -n)
    number_key="$1"
    number=$2
    shift 2
    ;;
  --regexp | -r)
    regexp_key=$1
    regexp=\"$2\"
    shift 2
    ;;
  --year-from | -from)
    year_from_key=$1
    year_from=$2
    shift 2
    ;;
  --year-to | -to)
    year_to_key=$1
    year_to=$2
    shift 2
    ;;
  --genres | -g)
    genres_key=$1
    genres=\"$2\"
    shift 2
    ;;
  esac
done


python3 get-movies.py $number_key $number $regexp_key $regexp $year_from_key $year_from $year_to_key $year_to $genres_key $genres