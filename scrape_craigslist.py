def scrape_craigslist(max_rent= None, min_rent = None, cat = 'apa'):

    from craigslist import CraigslistHousing
#     import filtering_functions
#     import zip_lookup
#     import neighbourhood_lookup
#     import math
#     from IPython.display import Markdown, display
#     def printmd(string):
#         display(Markdown(string))


    # Scrape Craigslist
    cl = CraigslistHousing(site='sfbay', area='sfc', category= cat)

    results = cl.get_results(geotagged=True, limit=50) #do we need to set a reasonable limit?

    with open('/home/w205/craigslist_scrape_tmp/scrape_temp.csv', 'w') as f:
        for result in results: # had to use a '>' as a delimiter so the geotag doesn't get split up
            csv_line = str(result['datetime']) + '>' + \
                str(result['geotag']) + '>' + \
                str(result['has_image']) + '>' + \
                str(result['has_map']) + '>' + \
                str(result['id']) + '>' + \
                str(result['name']) + '>' + \
                str(result['price']) + '>' + \
                str(result['url']) + '>' + \
                str(result['where'])
            f.write(csv_line)

scrape_craigslist()
