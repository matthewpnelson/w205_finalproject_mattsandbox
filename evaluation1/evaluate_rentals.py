# pull_table_in_spark.py
############################

from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext, SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.master("yarn").appName("my app").enableHiveSupport().getOrCreate()

conf = SparkConf().setAppName('Static Evaluations')
sc = SparkContext(conf=conf)
sqlContext = HiveContext(sc)

# Select Rentals from Hive Table
rentals_table_df = sqlContext.sql('SELECT * FROM unique_rentals')

# convert to dictionary
rentals = map(lambda row: row.asDict(), rentals_table_df.collect())


## **** need to import the functions we want to use ****
def f(entry):
    print(entry.Biz_Tally)

businesses_spark.foreach(f)
