DROP TABLE businesses;

CREATE EXTERNAL TABLE businesses
(
location_id string,
business_account_number string,
ownership_name string,
dba_name string,
street_address string,
city string,
state string,
source_zipcode string,
business_start_date date,
business_end_date date,
location_start_date date,
location_end_date date,
business_location string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/businesses';

DROP TABLE bike_parking;

CREATE EXTERNAL TABLE bike_parking
(
year_installed string,
month_installed string,
object_id string,
address string,
location string,
street string,
placement string,
number_of_racks int,
number_of_spaces int,
last_edited_date string,
geom string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/bike_parking';

DROP TABLE bike_stations;

CREATE EXTERNAL TABLE bike_stations
(
UID string,
site_id string,
station_location string,
location_name string,
phase string,
station_id string,
last_edited_date string,
geom string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/bike_stations';

DROP TABLE evictions;

CREATE EXTERNAL TABLE evictions
(
eviction_id string,
address string,
city string,
state string,
eviction_notice_source_zipcode string,
file_date string,
non_payment string,
breach string,
nuisance string,
illegal_use string,
failure_to_sign_renewal string,
access_denial string,
unapproved_subtenant string,
owner_move_in string,
demolition string,
capital_improvement string,
substantial_rehab string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
FIELDS ESCAPED BY '\\'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/evictions';

DROP TABLE fires;

CREATE EXTERNAL TABLE fires
(
incident_number string,
exposure_number string,
address string,
incident_date string,
call_number string,
alarm_datetime string,
arrival_datetime string,
close_datetime string,
city string,
zipcode string,
battalion string,
station_area string,
incident_box string,
suppression_units string,
suppression_personnel string,
ems_units string,
other_units string,
other_personnel string,
first_unit_on_scene string,
estimated_property_loss string,
estimated_contents_loss string,
fire_fatalities string,
fire_injuries string,
civilian_fatalities string,
civilian_injuries string,
number_of_alarms string,
primary_situation string,
mutual_aid string,
action_taken_primary string,
action_taken_secondary string,
action_taken_other string,
detector_alerted_occupants string,
property_use string,
area_of_fire_origin string,
ignition_cause string,
ignition_factor_primary string,
ignition_factor_secondary string,
heat_source string,
item_ignited_first string,
human_factors_associated_with_ignition string,
structure_type string,
structure_status string,
floor_of_fire_origin string,
fire_spread string,
no_flame_spread string,
number_of_floors_with_minimum_damage string,
number_of_floors_with_significant_damage string,
number_of_floors_with_heavy_damage string,
number_of_floors_with_extreme_damage string,
detectors_present string,
detector_type string,
detector_operation string,
detector_effectiveness string,
detector_failure_reason string,
automatic_extinguishing_system_present string,
automatic_extinguishing_system_type string,
automatic_extinguishing_system_performance string,
automatic_extinguishing_system_failure_reason string,
number_of_sprinkler_heads_operating string,
supervisor_district string,
neighborhood_district string,
location string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/fires';

DROP TABLE schools;

CREATE EXTERNAL TABLE schools
(
campus_name string,
ccsf_entity string,
upper_grade string,
grade_range string,
category string,
map_label string,
lower_age string,
upper_age string,
general_type string,
cds_code string,
campus_address string,
supervisor_district string,
county_fips string,
county_name string,
location_1 string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/schools';

DROP TABLE parking;

CREATE EXTERNAL TABLE parking
(
owner string,
address string,
prime_type string,
second_type string,
gar_or_lot string,
reg_cap string,
valet_cap string,
mc_cap string,
land_use_type string,
location_1 string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/parking';

DROP TABLE parks;

CREATE EXTERNAL TABLE parks
(
park_name string,
park_type string,
park_service_area string,
psa_manager string,
email string,
phone_number string,
zipcode string,
acreage string,
sup_dist string,
park_id string,
location_1 string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/parks';

DROP TABLE sfpd;

CREATE EXTERNAL TABLE sfpd
(
incident_num string,
category string,
description string,
day_of_week string,
incident_date string,
incident_time string,
pd_district string,
resolution string,
address string,
x_coord string,
y_coord string,
location string,
pd_id string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/sfpd';

DROP TABLE trees;

CREATE EXTERNAL TABLE trees
(
tree_id string,
legal_status string,
species string,
address string,
site_order string,
site_info string,
plant_type string,
caretaker string,
care_assistant string,
plant_date string,
dbh string,
plot_size string,
permit_notes string,
x_coord string,
y_coord string,
latitude string,
longitude string,
location string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/slackbot_static/trees';
