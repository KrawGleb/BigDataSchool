# Table with all movies
CREATE TABLE csv_files.movies
(
	movieID INT PRIMARY KEY,
    title VARCHAR(500),
    movieYear SMALLINT,
    genres VARCHAR(1000)
);
