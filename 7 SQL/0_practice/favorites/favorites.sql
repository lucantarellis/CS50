SELECT * FROM shows ORDER BY title;
UPDATE shows SET title = "How I Met Your Mother" WHERE title = "How i met your mother";
UPDATE shows SET title = "Adventure Time" WHERE title LIKE "adventure time";
UPDATE shows SET title = "Arrow" WHERE title LIKE "arrow";
UPDATE shows SET title = "Avatar: The Last Airbender" WHERE title LIKE "Avatar the%";
UPDATE shows SET title = "Brooklyn Nine-Nine" WHERE title LIKE "Brooklyn%" OR "B99";
UPDATE shows SET title = "Community" WHERE title LIKE "community";
UPDATE shows SET title = "Family Guy" WHERE title LIKE "family guy";
UPDATE shows SET title = "Friends" WHERE title LIKE "arrow";
