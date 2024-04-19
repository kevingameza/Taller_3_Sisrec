TRUNCATE TABLE users, songs, interactions, recomendations RESTART IDENTITY CASCADE;
COPY users (id, username, password, country) FROM '/var/lib/postgresql/csv-data/unique_users.csv' DELIMITER ';' CSV HEADER QUOTE '"' ESCAPE '\';
COPY songs (id, title, artist) FROM '/var/lib/postgresql/csv-data/unique_songs.csv' DELIMITER ';' CSV HEADER QUOTE '"' ESCAPE '\';
COPY interactions (user_id, item_id, rating) FROM '/var/lib/postgresql/csv-data/interaction.csv' DELIMITER ';' CSV HEADER QUOTE '"' ESCAPE '\';
COPY recomendations (user_id, item_id, pred, status) FROM '/var/lib/postgresql/csv-data/recommendations.csv' DELIMITER ';' CSV HEADER QUOTE '"' ESCAPE '\';
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('songs_id_seq', (SELECT MAX(id) FROM songs));
SELECT setval('interactions_id_seq', (SELECT MAX(id) FROM interactions));
SELECT setval('recomendations_id_seq', (SELECT MAX(id) FROM recomendations));