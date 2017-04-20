# static_evaluations.py
############################

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *


#sc = SparkContext("local", "businesses")
sc = SparkContext()
sqlContext = SQLContext(sc)

#results = sqlContext.sql('SELECT COUNT(business_account_number) FROM businesses \
#WHERE source_zipcode = GROUP BY business_account_number')
results = sqlContext.sql('SELECT business_account_number, source_zipcode FROM businesses LIMIT 10')
results.show()
