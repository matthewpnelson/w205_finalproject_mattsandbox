


# inputs from user
max_rent= 3000
min_rent = 2000
# min_rank_businesses = 1                 # 1 if you don't care about this, 10 if you really do
# min_rank_evictions = 1                  # 1 if you don't care about this, 10 if you really do
close_to_bike_parking = "Yes"          # Care about close bike parking, Yes or No
close_to_bike_station = "Yes"           # Care about close bike station, Yes or No
density_of_offstreet_parking = "Medium"
density_of_trees = "Medium"
density_of_schools = "Low" # SKIP FOR NOW, GEOTAG NOT IN HIVE TABLE?
density_of_SFPD_Incidents = "Medium"


# Low, Medium, High Density within Xkm (Select Low if you don't care)
                    # density_of_SFPD_Incidents = "High",       # Low, Medium, High Density in 2016 (Select High if you don't care)
                    # density_of_trees_100m = "Low")




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

    #############################################################
    # Select PARKS from Hive Table
    parks_table_df = sqlContext.sql('SELECT zipcode, count(park_name) as numparks FROM parks GROUP BY zipcode')
    # convert to dictionary
    parks_dict = map(lambda row: row.asDict(), parks_table_df.collect())
    parks = {each['zipcode']:each['numparks'] for each in parks_dict}

    # Select FIRES from Hive Table
    fires_table_df = sqlContext.sql('SELECT zipcode, count(incident_number) as numfires FROM fires GROUP BY zipcode')
    # convert to dictionary
    fires_dict = map(lambda row: row.asDict(), fires_table_df.collect())
    fires = {each['zipcode']:each['numfires'] for each in fires_dict}

    # Select Local Bars from Hive Table
    bars_table_df = sqlContext.sql('SELECT source_zipcode, count(dba_name) as numbars from businesses WHERE dba_name \
    LIKE "%Bar %" GROUP BY source_zipcode')
    # convert to dictionary
    bars_dict = map(lambda row: row.asDict(), bars_table_df.collect())
    bars = {each['source_zipcode']:each['numbars'] for each in bars_dict}

    # Select Local Restaurants
    restaurants_table_df = sqlContext.sql('SELECT source_zipcode, count(dba_name) as numrestaurants from businesses WHERE \
    dba_name LIKE "%Restaurant %" OR \
    dba_name LIKE "%Kitchen %" OR \
    dba_name LIKE "%Grill %" OR \
    dba_name LIKE "%Cuisine %" GROUP BY source_zipcode')
    # convert to dictionary
    restaurants_dict = map(lambda row: row.asDict(), restaurants_table_df.collect())
    restaurants = {each['source_zipcode']:each['numrestaurants'] for each in restaurants_dict}

    # Select all Businesses in zipcode
    businesses_table_df = sqlContext.sql('SELECT source_zipcode, count(dba_name) as numbusinesses from businesses WHERE \
    dba_name LIKE "%Restaurant %" OR \
    dba_name LIKE "%Kitchen %" OR \
    dba_name LIKE "%Grill %" OR \
    dba_name LIKE "%Cuisine %" GROUP BY source_zipcode')
    # convert to dictionary
    businesses_dict = map(lambda row: row.asDict(), businesses_table_df.collect())
    businesses = {each['source_zipcode']:each['numbusinesses'] for each in businesses_dict}


    #############################################################
    # Select BIKE PARKING from Hive Table
    bike_parking_table_df = sqlContext.sql('SELECT location, geom FROM bike_parking')
    # convert to dictionary
    bike_parking_dict = map(lambda row: row.asDict(), bike_parking_table_df.collect())
    bike_parking = {}
    for entry in bike_parking_dict: #dictionary comprehension wasn't working for some reason...
        try:
            geo = []
            for each in entry['geom'][1:-1].strip().split(","):
                geo.append(each)
            if len(geo) != 2:
                continue
            bike_parking[entry['location']] = geo
        except:
            continue

    #############################################################
    # Select BIKE STATIONS from Hive Table
    bike_stations_table_df = sqlContext.sql('SELECT location_name, geom FROM bike_stations')
    # convert to dictionary
    bike_stations_dict = map(lambda row: row.asDict(), bike_stations_table_df.collect())
    bike_stations = {}
    for entry in bike_stations_dict:
        try:
            geo = []
            for each in entry['geom'][1:-1].strip().split(","):
                geo.append(each)
            if len(geo) != 2:
                continue
            bike_stations[entry['location_name']] = geo
        except:
            continue


    #############################################################
    # Select SCHOOL LOCATIONS from Hive Table (GEOTAG NAME NOT CHANGED YET)
    schools_table_df = sqlContext.sql('SELECT campus_name, location_1 FROM schools')
    # convert to dictionary
    schools_dict = map(lambda row: row.asDict(), schools_table_df.collect())
    schools = {}
    for entry in schools_dict:
        try:
            geo = []
            for each in entry['location_1'][1:-1].strip().split(","):
                geo.append(each)
            if len(geo) != 2:
                continue
            schools[entry['campus_name']] = geo
        except:
            continue

    #############################################################
    # Select TREES from Hive Table
    trees_table_df = sqlContext.sql('SELECT tree_id, location FROM trees')
    # convert to dictionary
    trees_dict = map(lambda row: row.asDict(), trees_table_df.collect())
    trees = {}
    for entry in trees_dict:
        try:
            geo = []
            for each in entry['location'][1:-1].strip().split(","):
                geo.append(each)
            if len(geo) != 2:
                continue
            trees[entry['tree_id']] = geo
        except:
            continue

    #############################################################
    # Select SFPD from Hive Table
    sfpd_table_df = sqlContext.sql('SELECT incident_num, location FROM sfpd')
    # convert to dictionary
    sfpd_dict = map(lambda row: row.asDict(), sfpd_table_df.collect())
    sfpd = {}
    for entry in sfpd_dict:
        try:
            geo = []
            for each in entry['location'][1:-1].strip().split(","):
                geo.append(each)
            if len(geo) != 2:
                continue
            sfpd[entry['incident_num']] = geo
        except:
            continue


    #############################################################
    # Select PARKING LOCATIONS from Hive Table
    parking_table_df = sqlContext.sql('SELECT address, owner, reg_cap, location_1 FROM parking')
    # convert to dictionary
    parking_dict = map(lambda row: row.asDict(), parking_table_df.collect())
    parking = {}
    for entry in parking_dict:
        try:
            geo = []
            for each in entry['location_1'][1:-1].strip().split(","):
                geo.append(each)
            if len(geo) != 2:
                continue
            parking[entry['address']] = [entry['owner'], entry['reg_cap'], geo]
        except:
            continue


    #########################
    # Fake for now
    businesses_ranking = {'94102': 1, '11111': 5, '94104': 10, '94105': 10 }
    evictions_ranking = {'94102': 7, '11111': 4, '94104': 10, '94105': 9 }

    #
    # bike_share =   {'location 1': (37.7606289177, -122.410647009),
    #                 'location 2': (37.7855355791102, -122.411302813025),
    #                 'location 3': (37.7759676911831, -122.441396661871),
    #                 'location 4': (37.7518243814, -122.426627114),
    #                 'location 5': (37.75182438, -122.4266271)}

    # SFPD =      {'location 1': (37.7606289177, -122.410647009),
    #                 'location 2': (37.7855355791102, -122.411302813025),
    #                 'location 3': (37.7759676911831, -122.441396661871),
    #                 'location 4': (37.7518243814, -122.426627114),
    #                 'location 5': (37.75182438, -122.4266271)}
    #



    from check_rentals import check_rentals

    check_rentals(results = rentals,
                        businesses_ranking = businesses_ranking,              # Input Dictionary in form {zipcode: Rank}
                        evictions_ranking = evictions_ranking,               # Input Dictionary in form {zipcode: Rank}
                        bike_parking = bike_parking,
                        bike_stations = bike_stations,
                        tree_locations = trees,
                        school_locations = schools,
                        parking = parking,
                        parks_count = parks,
                        sfpd_locations = sfpd,
                        fires_count = fires,
                        bars_count = bars,
                        restaurants_count = restaurants,
                        businesses_count = businesses,

                        max_rent = max_rent,
                        min_rent = min_rent,
                        # min_rank_businesses = min_rank_businesses,                 # 1 if you don't care about this, 10 if you really do
                        # min_rank_evictions = min_rank_evictions,                  # 1 if you don't care about this, 10 if you really do
                        close_to_bike_parking = close_to_bike_parking,           # Care about close bike parking, Yes or No
                        close_to_bike_station = close_to_bike_station,
                        density_of_offstreet_parking = density_of_offstreet_parking, # Low, Medium, High Density within Xkm (Select Low if you don't care)))
                        density_of_trees = density_of_trees,
                        density_of_schools = density_of_schools,
                        density_of_SFPD_Incidents = density_of_SFPD_Incidents
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
