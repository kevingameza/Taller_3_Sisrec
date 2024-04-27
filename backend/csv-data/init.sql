TRUNCATE TABLE users, business, reviews, recommendations RESTART IDENTITY CASCADE;
COPY users (user_id, name, password) FROM '/var/lib/postgresql/csv-data/users.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';
COPY business (business_id, name, address, stars, postal_code, latitude, longitude) FROM '/var/lib/postgresql/csv-data/business_selected.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';
COPY reviews (review_id, user_id, business_id, stars, text, date) FROM '/var/lib/postgresql/csv-data/df_review.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';
COPY recommendations (user_id,business_id,stars, recommendation_id) FROM '/var/lib/postgresql/csv-data/predicciones_promedio.csv' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '\';

-- Adjust the sequence name if different
SELECT setval('recommendations_recommendation_id_seq', (SELECT MAX(recommendation_id) FROM recommendations) + 1);
