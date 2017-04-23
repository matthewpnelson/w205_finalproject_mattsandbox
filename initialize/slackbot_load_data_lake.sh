#!/bin/bash

# save my current directory
MY_CWD=$(pwd)

# create staging directory
mkdir ~/slackbot_staging

# change to staging directory
cd ~/slackbot_staging

# get medicare files from s3
wget https://s3.amazonaws.com/ucbmids205-slackbot-static/static_data2.zip
unzip static_data2.zip

# remove first line of files and rename
tail -n +3 Active_Business_Locations.csv > businesses.csv
mv Bicycle_Parking_Public.csv bike_parking.csv
mv Bike_Share_Stations.csv bike_stations.csv
mv Eviction_Notices.csv evictions.csv
mv Fire_Incidents.csv fires.csv
tail -n +2 Map_of_Schools.csv > schools.csv
mv Off-Street_parking_lots_and_parking_garages.csv parking.csv
mv Recreation___Park_Department_Park_Info_Dataset.csv parks.csv
mv SFPD_Incidents_Previous_Year_2016.csv sfpd.csv
mv Street_Tree_List.csv trees.csv
mv VItal_Signs_Commute_Time_City.csv commutes.csv
mv Vital_Signs__Home_Prices___by_zip_code.csv homes.csv

# create HDFS directories
hdfs dfs -mkdir /user/w205/slackbot_static
hdfs dfs -mkdir /user/w205/slackbot_static/businesses
hdfs dfs -mkdir /user/w205/slackbot_static/bike_parking
hdfs dfs -mkdir /user/w205/slackbot_static/bike_stations
hdfs dfs -mkdir /user/w205/slackbot_static/evictions
hdfs dfs -mkdir /user/w205/slackbot_static/fires
hdfs dfs -mkdir /user/w205/slackbot_static/schools
hdfs dfs -mkdir /user/w205/slackbot_static/parking
hdfs dfs -mkdir /user/w205/slackbot_static/parks
hdfs dfs -mkdir /user/w205/slackbot_static/sfpd
hdfs dfs -mkdir /user/w205/slackbot_static/trees
hdfs dfs -mkdir /user/w205/slackbot_static/commutes
hdfs dfs -mkdir /user/w205/slackbot_static/homes

# put files into HDFS
hdfs dfs -put businesses.csv /user/w205/slackbot_static/businesses
hdfs dfs -put bike_parking.csv /user/w205/slackbot_static/bike_parking
hdfs dfs -put bike_stations.csv /user/w205/slackbot_static/bike_stations
hdfs dfs -put evictions.csv /user/w205/slackbot_static/evictions
hdfs dfs -put fires.csv /user/w205/slackbot_static/fires
hdfs dfs -put schools.csv /user/w205/slackbot_static/schools
hdfs dfs -put parking.csv /user/w205/slackbot_static/parking
hdfs dfs -put parks.csv /user/w205/slackbot_static/parks
hdfs dfs -put sfpd.csv /user/w205/slackbot_static/sfpd
hdfs dfs -put trees.csv /user/w205/slackbot_static/trees
hdfs dfs -put commutes.csv /user/w205/slackbot_static/commutes
hdfs dfs -put homes.csv /user/w205/slackbot_static/homes

# change directory back to original
cd $MY_CWD

# clean exit
exit
