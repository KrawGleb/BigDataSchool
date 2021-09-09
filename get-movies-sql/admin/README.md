# Utility For Movies Selection (version for admins)

## Set up connection

There is configuration file in utils/config.ini. You can change all settings.
Please, don't forget to change your root password.

## Manual db init

### 1.Init tables

First you have to run scripts to create tables. These scripts are in SQL/DDL/Tables folder 

### 2.Init view

Create view. The required script is located SQL/DDL/Views folder

### 3.Create procedures

Create procedures The required script is located SQL/DDL/Procedures folder 

### 4.Data preparation

Download the dataset from the link https://grouplens.org/datasets/movielens/ and put the files movies.csv and ratings.csv in the folder /var/lib/mysql-files/

### 5.Populate tables

Call scripts the following scripts:
1. SQL/DML/Populate tables scripts/`load_movies_table.sql`
2. SQL/DML/Populate tables scripts/`load_ratings_table.sql`

### 6.Fill result table

Call `usp_fill_result_table` script