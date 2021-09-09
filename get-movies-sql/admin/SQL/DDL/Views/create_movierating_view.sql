USE csv_files;
CREATE VIEW movierating AS
SELECT 
	movies.movieID,
	movies.title,
    movies.movieYear,
    movies.genres,
    ROUND(AVG(ratings.rating), 2) AS rating
FROM movies
INNER JOIN ratings
ON movies.movieID = ratings.movieID
GROUP BY movies.movieId
ORDER BY AVG(ratings.rating) DESC, movies.movieYear DESC;
