#! /bin/bash

cd

# Start Hadoop
./start_hadoop.sh
/data/start_postgres.sh

# clone Github repo
git clone https://github.com/matthewpnelson/w205_finalproject_mattsandbox.git
cd w205_finalproject_mattsandbox/

# Manually Install Craigslist Scraper as root user
pip install python-craigslist --upgrade

# Set up Spark
cd initialize/
chmod +x setup_spark.sh
bash ./setup_spark.sh

# Set up PATH variables for SPARK
export SPARK=/data/spark15
export SPARK_HOME=$SPARK
export PATH=$SPARK/bin:$PATH

#start Hive Metastore
/data/start_metastore.sh

# download all static data, load data lake
chmod +x slackbot_load_data_lake.sh
./slackbot_load_data_lake.sh

# Run Hive DDL Statements to build static data tables
chmod +x slackbot_hive_base_ddl.sql
hive -f slackbot_hive_base_ddl.sql

# Run Spark to see if the Hive tables are there & Spark is synced up
##./data/spark15/bin/spark-sql

# run ranking scripts on some Hive Tables in Spark-SQL NOT FINISHED
#cd /data/spark15/bin/

# change to w205 user
su - w205
