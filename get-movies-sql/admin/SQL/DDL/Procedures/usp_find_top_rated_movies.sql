USE csv_files;
DELIMITER $$
CREATE PROCEDURE usp_find_top_rated_movies(IN n INT, IN re VARCHAR(500), IN year_from INT, IN year_to INT, IN genres VARCHAR(500))
BEGIN
	WITH RECURSIVE target_genres AS(
		SELECT 
			0 id,
			SUBSTRING_INDEX(SUBSTRING_INDEX(genres, '|', 1), '|', -1) AS genre
		UNION ALL
        SELECT 
			id+1,
			SUBSTRING_INDEX(SUBSTRING_INDEX(genres, '|', g.id+1), '|', -1)
        FROM target_genres AS g
        WHERE g.id < 20
    )
    SELECT 
		finally.genre,
        finally.title, 
        finally.movieYear,
        finally.rating
	FROM 
    (
		SELECT 
			r.genre AS genre,
			r.title AS title,
			r.movieYear AS movieYear,
			r.rating AS rating,
			ROW_NUMBER() OVER (PARTITION BY r.genre ORDER BY r.rating DESC, r.movieYear DESC, r.title) as rowNumber
		FROM result AS r
        WHERE
			r.title REGEXP(re)
            AND r.movieYear BETWEEN year_from AND year_to 
            AND (r.genre IN (SELECT genre FROM target_genres) OR genres IS NULL) 
    ) 
    AS finally
    WHERE (rowNumber <= n OR n IS NULL)
    ORDER BY genre, rating DESC, movieYear DESC, title;
END$$
