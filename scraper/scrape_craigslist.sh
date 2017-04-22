#!/bin/bash

# Make Directories if they don't already exist
mkdir /home/w205/craigslist_scrape_tmp
hdfs dfs -mkdir /user/w205/slackbot_static/craigslist_scrape_data

# Delete tmp csv file on local machine & HDFS
rm /home/w205/craigslist_scrape_tmp/scrape_temp.csv
hdfs dfs -rm /user/w205/slackbot_static/craigslist_scrape_data/scrape_temp.csv

# Run Scraping Script that saves results to a csv file
python scrape_craigslist.py

# Copy local tmp file to HDFS
hdfs dfs -put /home/w205/craigslist_scrape_tmp/scrape_temp.csv /user/w205/slackbot_static/craigslist_scrape_data

# Create tmp Hive Table from HDFS version
hive -f craigslist_tmp_ddl.sql

# Merge temp Table with Persistent Table
hive -f craigslist_merge.sql
