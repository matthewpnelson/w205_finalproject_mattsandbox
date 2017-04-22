


# inputs from user
max_rent= 6000
min_rent = 2000
min_rank_businesses = 1                 # 1 if you don't care about this, 10 if you really do
min_rank_evictions = 1                  # 1 if you don't care about this, 10 if you really do
close_to_bike_parking = "Yes",           # Care about close bike parking, Yes or No
density_of_offstreet_parking = "Medium" # Low, Medium, High Density within Xkm (Select Low if you don't care)
                    # density_of_SFPD_Incidents = "High",       # Low, Medium, High Density in 2016 (Select High if you don't care)
                    # density_of_trees_100m = "Low")






# Initialize Spark Context & Select Relevent Data From Hive Tables
# from pyspark import SparkContext, SparkConf
# from pyspark.sql import HiveContext
# from pyspark.sql import SparkSession
# from pyspark.sql.types import *
#
# spark = SparkSession.builder.master("yarn").appName("my app").enableHiveSupport().getOrCreate()
#
# conf = SparkConf().setAppName('Static Evaluations')
# sc = SparkContext(conf=conf)


#############################
# Rental Data
# Need in Form: output = {'id': '6060895324', 'has_map': True, 'price': '$1600', 'url': 'http://sfbay.craigslist.org/sfc/apa/6060895324.html',
#          'name': 'Furnished Room', 'has_image': True, 'datetime': '2017-03-26 09:33', 'where': 'nob hill', 'geotag': (37.790788, -122.419036)}

def main(sc):
    sqlContext = HiveContext(sc)

    # Select Rentals from Hive Table
    rentals_table_df = sqlContext.sql('SELECT * FROM unique_rentals')

    # convert to dictionary
    rentals = map(lambda row: row.asDict(), rentals_table_df.collect())


    #############################
    # Businesses Ranking Table
    # Need in Form: businesses_ranking = {'94102': 1, '11111': 5, '94104': 10, '94105': 10 }

    # Select Businesses Ranking from Hive Table
    # businesses_ranking_df = sqlContext.sql('SELECT * FROM businesses_ranking')
    # convert to dictionary
    # businesses_ranking = map(lambda row: row.asDict(), businesses_ranking_df.collect())

    # Select Bike Parking from Hive Table
    bike_parking_table_df = sqlContext.sql('SELECT location, geom FROM bike_parking')

    # convert to dictionary
    bike_parking_dict = map(lambda row: row.asDict(), bike_parking_table_df.collect())
    bike_parking = {}
    for entry in bike_parking_dict:
        geo = []
        for each in entry['geom'][1:-1].strip().split(","):
            geo.append(float(each))
        # geo = (entry['geom'][1:-1].strip().split(","))
        bike_parking[entry['location']] = geo
# print(bike_parking)
    # {entry['location']:entry['geom'] for entry in bike_parking_dict} dictionary comprehension not working in Spark-submit?

    #########################
    # Fake for now
    businesses_ranking = {'94102': 1, '11111': 5, '94104': 10, '94105': 10 }
    evictions_ranking = {'94102': 7, '11111': 4, '94104': 10, '94105': 9 }

    # bike_parking = {'location 1': (37.7606289177, -122.410647009),
    #                 'location 2': (37.7855355791102, -122.411302813025),
    #                 'location 3': (37.7759676911831, -122.441396661871),
    #                 'location 4': (37.7518243814, -122.426627114),
    #                 'location 5': (37.75182438, -122.4266271)}
    #
    # bike_share =   {'location 1': (37.7606289177, -122.410647009),
    #                 'location 2': (37.7855355791102, -122.411302813025),
    #                 'location 3': (37.7759676911831, -122.441396661871),
    #                 'location 4': (37.7518243814, -122.426627114),
    #                 'location 5': (37.75182438, -122.4266271)}

    off_street_parking =      {'location 1': ["Private", 13, (37.7606289177, -122.410647009)],
                    'location 2': ["Private", 15, (37.7855355791102, -122.411302813025)],
                    'location 3': ["Public", 18, (37.7759676911831, -122.441396661871)],
                    'location 4': ["Private", 27, (37.7518243814, -122.426627114)],
                    'location 5': ["Private", 60, (37.75182438, -122.4266271)]}

    # SFPD =      {'location 1': (37.7606289177, -122.410647009),
    #                 'location 2': (37.7855355791102, -122.411302813025),
    #                 'location 3': (37.7759676911831, -122.441396661871),
    #                 'location 4': (37.7518243814, -122.426627114),
    #                 'location 5': (37.75182438, -122.4266271)}
    #
    # trees =      {'location 1': (37.7606289177, -122.410647009),
    #                 'location 2': (37.7855355791102, -122.411302813025),
    #                 'location 3': (37.7759676911831, -122.441396661871),
    #                 'location 4': (37.7518243814, -122.426627114),
    #                 'location 5': (37.75182438, -122.4266271)}


    from check_rentals import check_rentals

    check_rentals(results = rentals,
                        businesses_ranking = businesses_ranking,              # Input Dictionary in form {zipcode: Rank}
                        evictions_ranking = evictions_ranking,               # Input Dictionary in form {zipcode: Rank}
                        bike_parking = bike_parking,

                        max_rent= max_rent,
                        min_rent = min_rent,
                        min_rank_businesses = min_rank_businesses,                 # 1 if you don't care about this, 10 if you really do
                        min_rank_evictions = min_rank_evictions,                  # 1 if you don't care about this, 10 if you really do
                        close_to_bike_parking = close_to_bike_parking,           # Care about close bike parking, Yes or No
                        density_of_offstreet_parking = density_of_offstreet_parking # Low, Medium, High Density within Xkm (Select Low if you don't care)))
                    )


## Spark Application - execute with spark-submit

## Imports
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext
#from pyspark.sql import SparkSession
from pyspark.sql.types import *

## Module Constants
APP_NAME = "Static Evaluations"

## Closure Functions

## Main functionality

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    # Execute Main functionality
    main(sc)
