USE csv_files;
TRUNCATE movies;
LOAD DATA INFILE '/var/lib/mysql-files/movies.csv'
INTO TABLE movies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(movieId, title, genres)
SET movieYear = SUBSTR(REGEXP_SUBSTR(title, '[(|–][0-9]{4}[)]'), 2, 4),
title = IF(title REGEXP('[(][0-9]{4}[)]'), SUBSTR(title, 1, LENGTH(title)-6), title);
