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

def min_in_zip(zip_eval_dict):
    minimum = None
    maximum = None
    for zipcode, count in zip_eval_dict.items():
        if count < minimum or minimum == None:
            minimum = count
        if count > maximum or maximum == None:
            maximum = count
    return minimum, maximum

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
    MAX_BIKE_DIST = 0.5 # kilometers

    for spot, coords in bike_parking_locations.items():
        dist = points2distance(coords,geotag)
        if (min_dist is None or dist < min_dist) and dist < MAX_BIKE_DIST:
            bike = spot
            near_bike = True
            min_dist = dist
    return near_bike, bike, min_dist

# Find closest Bike Station
def close_to_bike_station(geotag, bike_parking_locations):

    min_dist = None
    near_bike = False
    bike_dist = "N/A"
    bike = ""
    MAX_BIKE_DIST = 1 # kilometers

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
    MAX_PARK_DIST = 1 # kilometers
    low_density_threshold = 100
    med_density_threshold = 500

    # Loop through Parking Locations and sum total available spots (within Max Distance of geotag) for both Private/Public
    for name, info in parking_locations.items():
        dist = points2distance(info[2],geotag)
        if dist < MAX_PARK_DIST and info[0] != "Private":
            public_parking_count += int(info[1]) # Assuming the Parking lot info has # of spots in the raw data
        elif dist < MAX_PARK_DIST and info[0] == "Private":
            private_parking_count += int(info[1])
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


def school_density(geotag, school_locations):

    school_count = 0
    MAX_SCHOOL_DIST = 10 # kilometers
    low_density_threshold = 3
    med_density_threshold = 10

    # Loop through school Locations and sum total available spots (within Max Distance of geotag) for both Private/Public
    for name, coords in school_locations.items():
        dist = points2distance(coords,geotag)
        if dist < MAX_SCHOOL_DIST:
            school_count += 1
        else:
            continue

    # Characterize Public school Density
    school_density = None
    if school_count > 0 and school_count <= low_density_threshold:
        school_density = "Low School Density"
    elif school_count > low_density_threshold and school_count <= med_density_threshold:
        school_density = "Medium School Density"
    elif school_count > med_density_threshold:
        school_density = "High School Density"

    return school_density, school_count

def sfpd_density(geotag, sfpd_locations):

    sfpd_count = 0
    MAX_SFPD_DIST = 1 # kilometers
    low_density_threshold = 5000
    med_density_threshold = 10000

    # Loop through sfpd Locations and sum total available spots (within Max Distance of geotag) for both Private/Public
    for name, coords in sfpd_locations.items():
        dist = points2distance(coords,geotag)
        if dist < MAX_SFPD_DIST:
            sfpd_count += 1
        else:
            continue

    # Characterize Public sfpd Density
    sfpd_density = None
    if sfpd_count > 0 and sfpd_count <= low_density_threshold:
        sfpd_density = "Low SFPD Density"
    elif sfpd_count > low_density_threshold and sfpd_count <= med_density_threshold:
        sfpd_density = "Medium SFPD Density"
    elif sfpd_count > med_density_threshold:
        sfpd_density = "High SFPD Density"

    return sfpd_density, sfpd_count


def tree_density(geotag, tree_locations):

    tree_count = 0
    MAX_TREE_DIST = 1 # kilometers
    low_density_threshold = 1000
    med_density_threshold = 10000

    # Loop through tree Locations and sum total
    for name, coords in tree_locations.items():
        dist = points2distance(coords,geotag)
        if dist < MAX_TREE_DIST:
            tree_count += 1
        else:
            continue

    # Characterize Public tree Density
    tree_density = None
    if tree_count > 0 and tree_count <= low_density_threshold:
        tree_density = "Low Tree Density"
    elif tree_count > low_density_threshold and tree_count <= med_density_threshold:
        tree_density = "Medium Tree Density"
    elif tree_count > med_density_threshold:
        tree_density = "High Tree Density"

    return tree_density, tree_count
