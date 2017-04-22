# Convert Dollar String to int
def parse_dollar_sign(string):
    int(each['price'].replace("$",""))

# Acceptable Zip Codes by SQL Query results

def check_businesses(min_rank, businesses_ranking_dict_by_zipcode):
    zips = []
    for zipcode, rank in businesses_ranking_dict_by_zipcode.items():

        # not needed if we avoid entering this function in the main scraper script
        if min_rank == None:
            zips.append(zipcode)
            continue

        # add valid zip codes that meet the minimum rank
        if rank >= min_rank:
            zips.append(zipcode)
    if zips == []:
        zips == None
    return zips

def check_evictions(min_rank, evictions_ranking_dict_by_zipcode):
    zips = []
    for zipcode, rank in evictions_ranking_dict_by_zipcode.items():

        # not needed if we avoid entering this function in the main scraper script
        if min_rank == None:
            zips.append(zipcode)
            continue

        # add valid zip codes that meet the minimum rank
        if rank >= min_rank:
            zips.append(zipcode)
    if zips == []:
        zips == None
    return zips

def check_schools_k9(min_rank, k9schools_ranking_dict_by_zipcode):
    zips = []
    for zipcode, rank in k9schools_ranking_dict_by_zipcode.items():

        # not needed if we avoid entering this function in the main scraper script
        if min_rank == None:
            zips.append(zipcode)
            continue

        # add valid zip codes that meet the minimum rank
        if rank >= min_rank:
            zips.append(zipcode)
    if zips == []:
        zips == None
    return zips

def check_schools_hs(min_rank, hsschools_ranking_dict_by_zipcode):
    zips = []
    for zipcode, rank in hsschools_ranking_dict_by_zipcode.items():

        # not needed if we avoid entering this function in the main scraper script
        if min_rank == None:
            zips.append(zipcode)
            continue

        # add valid zip codes that meet the minimum rank
        if rank >= min_rank:
            zips.append(zipcode)
    if zips == []:
        zips == None
    return zips

def check_home_prices(min_rank, home_prices_ranking_dict_by_zipcode):
    zips = []
    for zipcode, rank in home_prices_ranking_dict_by_zipcode.items():

        # not needed if we avoid entering this function in the main scraper script
        if min_rank == None:
            zips.append(zipcode)
            continue

        # add valid zip codes that meet the minimum rank
        if rank >= min_rank:
            zips.append(zipcode)
    if zips == []:
        zips == None
    return zips




# Calculate Distance to _ functions
# Adapted from http://www.codecodex.com/wiki/Calculate_distance_between_two_points_on_a_globe#Python
import math
def points2distance(start,  end):
    """
    Calculate distance (in kilometers) between two points given as (long, latt) pairs
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    """
    print(start)
    end_latt = math.radians(float(end[0]))
    end_long = math.radians(float(end[1]))
    start_latt = math.radians(float(start[0]))
    start_long = math.radians(float(start[1]))

    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c

# Find closest Bike Parking
def close_to_bike_parking(geotag, bike_parking_locations):

    min_dist = None
    near_bike = False
    bike_dist = "N/A"
    bike = ""
    MAX_BIKE_DIST = 20 # kilometers

    for spot, coords in bike_parking_locations.items():
        dist = points2distance(coords,geotag)
        if (min_dist is None or dist < min_dist) and dist < MAX_BIKE_DIST:
            bike = spot
            near_bike = True
            min_dist = dist
    return near_bike, bike, min_dist

def parking_density(geotag, parking_locations):

    public_parking_count = 0
    private_parking_count = 0
    MAX_PARK_DIST = 20 # kilometers
    low_density_threshold = 20
    med_density_threshold = 100

    # Loop through Parking Locations and sum total available spots (within Max Distance of geotag) for both Private/Public
    for name, info in parking_locations.items():
        dist = points2distance(info[2],geotag)
        if dist < MAX_PARK_DIST and info[0] == "Public":
            public_parking_count += info[1] # Assuming the Parking lot info has # of spots in the raw data
        elif dist < MAX_PARK_DIST and info[0] == "Private":
            private_parking_count += info[1]
        else:
            continue

    # Characterize Public Parking Density
    public_parking_density = None
    if public_parking_count > 0 and public_parking_count <= low_density_threshold:
        public_parking_density = "Low Public Parking Density"
    elif public_parking_count > low_density_threshold and public_parking_count <= med_density_threshold:
        public_parking_density = "Medium Public Parking Density"
    elif public_parking_count > med_density_threshold:
        public_parking_density = "High Public Parking Density"

    # Characterize Private Parking Density
    private_parking_density = None
    if private_parking_count > 0 and private_parking_count <= low_density_threshold:
        private_parking_density = "Low Private Parking Density"
    elif private_parking_count > low_density_threshold and private_parking_count <= med_density_threshold:
        private_parking_density = "Medium Private Parking Density"
    elif private_parking_count > med_density_threshold:
        private_parking_density = "High Private Parking Density"

    return public_parking_density, public_parking_count, private_parking_density, private_parking_count
