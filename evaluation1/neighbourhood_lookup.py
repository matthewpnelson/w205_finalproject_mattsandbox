# Neighbourhood Bounding Boxes for Neighbourhood Lookups

# Function to Take a list of latlong polygons with associated neighbourhood names and turn into a dictionary with key = neighbourhood
def import_NH_polygons(filename = 'SFFind_Neighborhoods.csv'):
    import csv
    with open(filename, 'rt') as fin:
        reader = csv.reader(fin, delimiter=',')
        latlong = []
        neighbourhood = []
        for row in reader:
            if row[1][0:12] == 'MULTIPOLYGON':
                latlong.append(row[1][16:-3].split(","))
                neighbourhood.append(row[2])
        new_latlong = {}
        i = 0
        while i < len(neighbourhood):
            entry = []
            for LL in latlong[i]:
                str_tup = tuple(float(item) for item in LL.strip().split(" "))
                entry.append(str_tup)
            new_latlong[neighbourhood[i]] = entry
            i += 1
        #for each in latlong:
        #    entry = []
        #    for LL in each:
        #        str_tup = tuple(LL.strip().split(" "))
        #        entry.append(str_tup)
        #    new_latlong.append(entry)
            #print(tuple(str(each).split(" ",1)))
        return new_latlong

# Function to get min and max lat long from each neighbourhood box (to approximate a square...)
def NH_BOXES(NH_polygons = import_NH_polygons()):
    BOXES = {}
    for neighbourhood, polygon in NH_polygons.items():
        for entry in polygon:
            running_min_lat = entry[-1]
            running_max_lat = entry[-1]
            running_min_long = entry[0]
            running_max_long = entry[0]
            break
        for entry in polygon:
            if entry[0] < running_min_long and entry[0] <= -120 and entry[0] > -123:
                running_min_long = entry[0]
            if entry[0] > running_max_long and entry[0] <= -120 and entry[0] > -123:
                running_max_long = entry[0]
            if entry[-1] < running_min_lat and entry[-1] <= 39 and entry[-1] > 36:
                running_min_lat = entry[-1]
            if entry[-1] > running_max_lat and entry[-1] <= 39 and entry[-1] > 36:
                running_max_lat = entry[-1]

        BOXES[neighbourhood] = [[running_min_lat, running_max_long], #min lat & max long = top right corner
                         [running_max_lat, running_min_long]] #max lat & min long = bottom left corner
    return BOXES

BOXES = NH_BOXES()


# BOXES = {
#     "adams_point": [
#         [37.80789, -122.25000],
#         [37.81589,	-122.26081]
#     ],
#     "piedmont": [
#         [37.82240, -122.24768],
#         [37.83237, -122.25386]
#     ],
#     "Other Neighbourhood": [
#         [35, -121],
#         [39, -123]
#     ]
# }

# Function to check if a geotag is in a bounding box
def in_box(coords, box):
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False

def neighbourhood_lookup(geotag):
    for neighbourhood, coords in BOXES.items():
        if in_box(geotag, coords):
            hood = neighbourhood
            return hood
    return None



# Name based Neighbourhood Lookups in case Listing does not have geotag
NEIGHBORHOODS = ["berkeley north", "berkeley", "rockridge", "adams point"]
