# static_evaluations.py
############################

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *


sc = SparkContext("local", "Static Evaluations")
sqlContext = SQLContext(sc)

# Businesses Ranking
########################################################
businesses_spark = sqlContext.sql('SELECT source_zipcode, COUNT(business_account_number) FROM businesses \
                                GROUP BY source_zipcode ORDER BY DESC')
businesses_spark.show()


# someone fill in this code to build a list of zip codes in each ranking #
# maybe use blocks? ie. 0-10 businesses = 1, 11-20 businesses = 2, etc?

businesses_ranking = {"1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[]}


# Nearby Schools
########################################################



# Other
########################################################




# Other
########################################################
