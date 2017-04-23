def check_rentals(results,
                    businesses_ranking,              # Input Dictionary in form {zipcode: Rank}
                    evictions_ranking,               # Input Dictionary in form {zipcode: Rank}
                    #schools_k9_ranking,               # Input Dictionary in form {zipcode: Rank}
                    #schools_hs_ranking,              # Input Dictionary in form {zipcode: Rank}
                    bike_parking,


                    max_rent= None,
                    min_rent = None,

                    min_rank_businesses = 1,                 # 1 if you don't care about this, 10 if you really do
                    min_rank_evictions = 1,                  # 1 if you don't care about this, 10 if you really do
                    min_rank_schools_k9 = 1,                 # 1 if you don't care about this, 10 if you really do
                    min_rank_schools_hs = 1,                 # 1 if you don't care about this, 10 if you really do
                    # skip for now, min_rank_home_prices = 1,                # 1 if you don't care about this, 10 if you really do
                    close_to_bike_parking = "Yes",           # Care about close bike parking, Yes or No
                    distance_to_bike_share = "Short",        # Short, Medium, Long (Select Long if you don't care)
                    density_of_offstreet_parking = "Low", # Low, Medium, High Density within Xkm (Select Low if you don't care)
                    density_of_SFPD_Incidents = "High",       # Low, Medium, High Density in 2016 (Select High if you don't care)
                    density_of_trees_100m = "Low"):          # Low, Medium, High Density within 500m (Select Low if you don't care):

    '''Script used to filter all craigslist rentals according to user preferences.

    User Preferences are set as defaults where the filter will no longer be applied:
    '''

    from craigslist import CraigslistHousing
    import filtering_functions
    import zip_lookup
    import neighbourhood_lookup
    import math

    tentative_rental = []
    valid_rentals = []
    for result in results:
        print("Evaluating: ", result['name'], result['url'])
        ################################################################################################
        ### INITIALIZE RESULT

        # assign geotag if it is provided in the rental ad
        if result['geotag'] is not None:
            geotag = result['geotag']
            geotag = []
            for each in result['geotag'][1:-1].strip().split(","):
                geotag.append(each)
            if len(geotag) != 2:
                continue
        else:
            continue #skip for now because there is no geotag

        zipcode = zip_lookup.zip_lookup_by_geotag(geotag)
        tentative_rental.append(result)

        ### Get Approximate Neighbourhood by Geotag
        if result["location"] != None:
            result["area"] = result["location"]
        else:
            result["area"] = neighbourhood_lookup.neighbourhood_lookup(geotag)


        ################################################################################################
        ### APPLY FILTERS

        #-----------------------------------------------------------------------------------------------
        ## DIRECT FILTERS
        #-----------------------------------------------------------------------------------------------

        # MAX PRICE
        if max_rent == None:
            pass
        else:
            try:
                if int(result['price'].replace("$","")) > max_rent:
                    continue #doesn't meet user criteria, go on to next result
            except:
                continue

        # MIN PRICE
        if min_rent == None:
            pass
        else:
            try:
                if int(result['price'].replace("$","")) < min_rent:
                    continue #doesn't meet user criteria, go on to next result
            except:
                continue


        #-----------------------------------------------------------------------------------------------
        ## ZIPCODE BASED FILTERS
        #-----------------------------------------------------------------------------------------------

        # # OF BUSINESSES
        if min_rank_businesses == 1:
            pass
        else:
            if zipcode not in filtering_functions.check_businesses(min_rank_businesses, businesses_ranking):
                continue #doesn't meet user criteria, go on to next result

        # NEARBY SCHOOLS
        if min_rank_evictions == 1:
            pass
        else:
            if zipcode not in filtering_functions.check_evictions(min_rank_evictions, evictions_ranking):
                continue #doesn't meet user criteria, go on to next result

        #-----------------------------------------------------------------------------------------------
        ## DISTANCE BASED FILTERS
        #-----------------------------------------------------------------------------------------------

        #----------------------------------
        ## DISTANCE TO X FILTERS
        #----------------------------------

        # BIKE PARKING (is bike parking within 20km of the rental? (huge window until we get actual locations loaded))
        if close_to_bike_parking == "No":
            result["BP_close"] = "N/A"
            result["BP_location"] = "N/A"
            result["BP_distance"] = "N/A"

            pass #skip this filter, user doesn't care
        else:
            BP_close, BP_location, BP_distance = filtering_functions.close_to_bike_parking(geotag, bike_parking)
            if BP_close == False:
                continue #doesn't meet user criteria, go on to next result
            else:
                result["BP_close"] = BP_close
                result["BP_location"] = BP_location
                result["BP_distance"] = BP_distance


        #----------------------------------
        ## DENSITY STYLE FILTERS
        #----------------------------------

        # VEHICLE PARKING DENSITY (Initial Parking window set @ 20km, huge window until we get actual locations loaded)
        if density_of_offstreet_parking == "Low":
            pass #skip this filter, user doesn't care
        else:
            Public_Parking_Density, Public_Parking_Spots, Private_Parking_Density, \
                Private_Parking_Spots = filtering_functions.parking_density(geotag,off_street_parking)
            if (Public_Parking_Density == "High Public Parking Density" or Private_Parking_Density == "High Private Parking Density") and density_of_offstreet_parking == "High":
                result["Public_Parking_Density"], result["Public_Parking_Spots"], result["Private_Parking_Density"], \
                result["Private_Parking_Spots"] = filtering_functions.parking_density(geotag,off_street_parking)
            elif (Public_Parking_Density in ("High Public Parking Density","Medium Public Parking Density") \
                or Private_Parking_Density in ("High Private Parking Density","Medium Private Parking Density")) \
                and density_of_offstreet_parking == "Medium":
                result["Public_Parking_Density"], result["Public_Parking_Spots"], result["Private_Parking_Density"], \
                result["Private_Parking_Spots"] = filtering_functions.parking_density(geotag,off_street_parking)
            else:
                continue #doesn't meet user criteria, go on to next result




        ################################################################################################
        # Made it to the end of the filters intact? Rental is Valid for this User's Query!
        valid_rentals.append(result)
        tentative_rental = [] # reset the tentative rental, continue loop

        ################################################################################################
        ### DISPLAY VALID RESULTS
        #printmd('**-------------------VALID RESULT------------------**')
        print("****************VALID RESULT************")
        print("Area: ", result["area"], "\n",
              "Price: ", result["price"], "\n",
              "Listing Name: ", result["name"], "\n",
              "URL: ", result["url"], "\n",
              "Bike Parking (Close?, Location Name, Distance (km)): ",result["BP_close"], result["BP_location"], result["BP_distance"], "\n")
            #   "Local Public Off-Street Parking Density, # of Spots: ", result["Public_Parking_Density"], result["Public_Parking_Spots"], "\n",
            #   "Local Private Off-Street Parking Density, # of Spots: ",result["Private_Parking_Density"], result["Private_Parking_Spots"])
        print("****************************************")
        #printmd('**-------------------------------------------------**')

        ### POST TO SLACK
        from slackclient import SlackClient
        import evaluation_settings

        SLACK_TOKEN = evaluation_settings.SLACK_TOKEN
        SLACK_CHANNEL = evaluation_settings.SLACK_CHANNEL

        sc = SlackClient(SLACK_TOKEN)
        desc = "Area: " + str(result["area"]) +  "\n" + \
              "Price: " +  str(result["price"]) +  "\n" + \
              "Listing Name: " +  str(result["name"]) +  "\n" + \
              "URL: " +  str(result["url"]) +  "\n" + \
              "Bike Parking (Close?, Location Name, Distance (km)): " + str(result["BP_close"]) +  str(result["BP_location"]) +  str(result["BP_distance"]) +  "\n" # + \
            #   "Local Public Off-Street Parking Density, # of Spots: " +  result["Public_Parking_Density"] +  result["Public_Parking_Spots"] +  "\n" + \
            #   "Local Private Off-Street Parking Density, # of Spots: " + result["Private_Parking_Density"] +  result["Private_Parking_Spots"]

        desc= "************************HERE IS A LISTING THAT MEETS YOUR CRITERIA********************* \n \
        Area: {0} km \n \
        Price: {1} \n \
        Listing Name: {2} \n \
        URL: <{3}> \n \
        Bike Parking Close? {4} \n \
        Closest Bike Parking Location: {5} \n \
        Distance to Closest Bike Parking Location: {6} km \n \
        ****************************************************************************************".format(result["area"],result["price"],result["name"],result["url"],result["BP_close"],result["BP_location"],round(result["BP_distance"],2))

        # desc = "{0} | {1} | {2} | {3} | <{4}>".format(result["area"], result["price"], result["name"], result["url"])
        sc.api_call(
            "chat.postMessage", channel=SLACK_CHANNEL, text=desc,
            username='pybot', icon_emoji=':robot_face:'
        )

    #return valid_rentals
