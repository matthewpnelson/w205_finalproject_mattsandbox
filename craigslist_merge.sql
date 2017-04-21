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
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/craigslist_scrape_data';

CREATE TABLE craigslist_rentals AS
SELECT * FROM craigslist_rentals UNION SELECT * FROM craigslist_data_tmp;
