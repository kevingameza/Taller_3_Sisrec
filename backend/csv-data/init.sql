TRUNCATE TABLE users, movies, ratings, tags, recommendations RESTART IDENTITY CASCADE;
COPY users (user_id, password) FROM '/var/lib/postgresql/csv-data/users.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';
COPY movies (movie_id,title,genres,stars,directors,startyear,isadult) FROM '/var/lib/postgresql/csv-data/movies.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';
COPY ratings (rating_id, user_id, movie_id, rating) FROM '/var/lib/postgresql/csv-data/ratings.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';
COPY tags (tag_id, user_id, movie_id, tag) FROM '/var/lib/postgresql/csv-data/tags.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';

-- COPY recommendations (user_id,business_id,stars, recommendation_id) FROM '/var/lib/postgresql/csv-data/predicciones_promedio.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';

-- Adjust the sequence name if different
-- SELECT setval('recommendations_recommendation_id_seq', (SELECT MAX(recommendation_id) FROM recommendations) + 1);
