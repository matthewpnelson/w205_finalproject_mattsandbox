CREATE TABLE IF NOT EXISTS craigslist_rentals
(
datetime date,
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
SELECT DISTINCT * FROM craigslist_data_tmp
FROM craigslist_data_tmp A
LEFT JOIN craigslist_rentals B
ON craigslist_data_tmp.posting_id = craigslist_rentals.posting_id
WHERE craigslist_rentals.posting_id IS NULL;

-- CREATE TABLE craigslist_rentals AS
-- SELECT * FROM craigslist_rentals
-- UNION
-- SELECT * FROM craigslist_data_tmp;
