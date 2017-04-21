CREATE TABLE IF NOT EXISTS craigslist_rentals
(
posted_date date,
geotag string,
has_image string,
has_map string,
posting_id string,
name string,
price int,
url string,
location string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ">",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/craigslist_scrape_data';

INSERT INTO craigslist_rentals
(
craigslist_rentals.posted_date,
craigslist_rentals.geotag,
craigslist_rentals.has_image,
craigslist_rentals.has_map,
craigslist_rentals.posting_id,
craigslist_rentals.name,
craigslist_rentals.price,
craigslist_rentals.url,
craigslist_rentals.location
)
SELECT DISTINCT craigslist_data_tmp.posted_date,
craigslist_data_tmp.geotag,
craigslist_data_tmp.has_image,
craigslist_data_tmp.has_map,
craigslist_data_tmp.posting_id,
craigslist_data_tmp.name,
craigslist_data_tmp.price,
craigslist_data_tmp.url,
craigslist_data_tmp.location
FROM craigslist_data_tmp
LEFT JOIN craigslist_rentals
ON craigslist_data_tmp.name = craigslist_rentals.name
WHERE craigslist_rentals.name IS NULL;

-- CREATE TABLE craigslist_rentals AS
-- SELECT * FROM craigslist_rentals
-- UNION
-- SELECT * FROM craigslist_data_tmp;
