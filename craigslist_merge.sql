CREATE TABLE IF NOT EXISTS craigslist_rentals;

CREATE TABLE craigslist_rentals AS
SELECT * FROM craigslist_rentals UNION SELECT * FROM craigslist_data_tmp;
