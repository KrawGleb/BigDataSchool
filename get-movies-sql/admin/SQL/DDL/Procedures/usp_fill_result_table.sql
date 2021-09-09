USE csv_files;
DELIMITER $$
CREATE PROCEDURE usp_fill_result_table()
BEGIN
	TRUNCATE result;
    INSERT INTO result(title, movieYear, genre, rating)
	WITH RECURSIVE genres AS(
	SELECT
		0 id, 
		m.movieID,
		TRIM('\r' FROM SUBSTRING_INDEX(SUBSTRING_INDEX(m.genres, '|', 1), '|', -1)) AS genre 
	FROM movies AS m
	UNION ALL
	SELECT 
		g.id+1,
		m.movieID,
		TRIM('\r' FROM SUBSTRING_INDEX(SUBSTRING_INDEX(m.genres, '|', g.id+1), '|', -1))
	FROM genres AS g
	INNER JOIN movies AS m
	ON g.movieID = m.movieID
	WHERE id < 20
	) 
	SELECT DISTINCT 
		m.title,
		m.movieYear,
		g.genre,
        m.rating
	FROM genres AS g
	INNER JOIN movierating AS m
	ON 
	m.movieID = g.movieID
    ORDER BY m.rating DESC, m.movieYear DESC, m.title;
END$$


