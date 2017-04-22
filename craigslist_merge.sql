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


-- INSERT INTO craigslist_rentals
-- (
-- craigslist_rentals.posted_date,
-- craigslist_rentals.geotag,
-- craigslist_rentals.has_image,
-- craigslist_rentals.has_map,
-- craigslist_rentals.posting_id,
-- craigslist_rentals.name,
-- craigslist_rentals.price,
-- craigslist_rentals.url,
-- craigslist_rentals.location
-- )
-- SELECT DISTINCT
-- craigslist_data_tmp.posted_date,
-- craigslist_data_tmp.geotag,
-- craigslist_data_tmp.has_image,
-- craigslist_data_tmp.has_map,
-- craigslist_data_tmp.posting_id,
-- craigslist_data_tmp.name,
-- craigslist_data_tmp.price,
-- craigslist_data_tmp.url,
-- craigslist_data_tmp.location
-- FROM craigslist_data_tmp
-- LEFT JOIN craigslist_rentals
-- ON craigslist_data_tmp.posting_id = craigslist_rentals.posting_id
-- WHERE craigslist_rentals.posting_id IS NULL;
--


-- INSERT INTO unique_rentals
-- (
-- craigslist_rentals.posted_date,
-- craigslist_rentals.geotag,
-- craigslist_rentals.has_image,
-- craigslist_rentals.has_map,
-- craigslist_rentals.posting_id,
-- craigslist_rentals.name,
-- craigslist_rentals.price,
-- craigslist_rentals.url,
-- craigslist_rentals.location
-- )
-- SELECT DISTINCT
-- craigslist_data_tmp.posted_date,
-- craigslist_data_tmp.geotag,
-- craigslist_data_tmp.has_image,
-- craigslist_data_tmp.has_map,
-- craigslist_data_tmp.posting_id,
-- craigslist_data_tmp.name,
-- craigslist_data_tmp.price,
-- craigslist_data_tmp.url,
-- craigslist_data_tmp.location
-- FROM craigslist_data_tmp
-- LEFT JOIN craigslist_rentals
-- ON craigslist_data_tmp.posting_id = craigslist_rentals.posting_id
-- WHERE craigslist_rentals.posting_id IS NULL;
--
-- INSERT INTO unique_rentals
-- SELECT * FROM craigslist_rentals
-- UNION
-- SELECT * FROM craigslist_data_tmp;

DROP TABLE unique_rentals;

CREATE TABLE unique_rentals AS
SELECT
unique_rentals.posted_date,
unique_rentals.geotag,
unique_rentals.has_image,
unique_rentals.has_map,
unique_rentals.posting_id,
unique_rentals.name,
unique_rentals.price,
unique_rentals.url,
unique_rentals.location
FROM (
  SELECT DISTINCT
  craigslist_rentals.posted_date,
  craigslist_rentals.geotag,
  craigslist_rentals.has_image,
  craigslist_rentals.has_map,
  craigslist_rentals.posting_id,
  craigslist_rentals.name,
  craigslist_rentals.price,
  craigslist_rentals.url,
  craigslist_rentals.location
  FROM craigslist_rentals
  UNION ALL
  SELECT DISTINCT
  craigslist_data_tmp.posted_date,
  craigslist_data_tmp.geotag,
  craigslist_data_tmp.has_image,
  craigslist_data_tmp.has_map,
  craigslist_data_tmp.posting_id,
  craigslist_data_tmp.name,
  craigslist_data_tmp.price,
  craigslist_data_tmp.url,
  craigslist_data_tmp.location
  from craigslist_data_tmp
) unique_rentals;


-- Drop Temporary Copy
DROP TABLE craigslist_rentals;


-- Copy Table
CREATE TABLE craigslist_rentals AS SELECT * FROM unique_rentals;



-- INSERT INTO craigslist_rentals
-- SELECT
-- craigslist_rentals.posted_date,
-- craigslist_rentals.geotag,
-- craigslist_rentals.has_image,
-- craigslist_rentals.has_map,
-- craigslist_rentals.posting_id,
-- craigslist_rentals.name,
-- craigslist_rentals.price,
-- craigslist_rentals.url,
-- craigslist_rentals.location
-- FROM (
--   SELECT
--   craigslist_rentals.posted_date,
--   craigslist_rentals.geotag,
--   craigslist_rentals.has_image,
--   craigslist_rentals.has_map,
--   craigslist_rentals.posting_id,
--   craigslist_rentals.name,
--   craigslist_rentals.price,
--   craigslist_rentals.url,
--   craigslist_rentals.location
--   FROM craigslist_rentals
--   UNION ALL
--   SELECT
--   craigslist_data_tmp.posted_date,
--   craigslist_data_tmp.geotag,
--   craigslist_data_tmp.has_image,
--   craigslist_data_tmp.has_map,
--   craigslist_data_tmp.posting_id,
--   craigslist_data_tmp.name,
--   craigslist_data_tmp.price,
--   craigslist_data_tmp.url,
--   craigslist_data_tmp.location
--   FROM craigslist_data_tmp
-- ) craigslist_rentals;
