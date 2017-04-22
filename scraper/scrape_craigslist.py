import scraper_settings
from slackclient import SlackClient

def scrape_craigslist():

    from craigslist import CraigslistHousing

    # Scrape Craigslist
    cl = CraigslistHousing(site='sfbay', area=["eby", "sfc", "sby", "nby"], category='apa')

    results = cl.get_results(geotagged=True, limit=100) #do we need to set a reasonable limit?
#sort_by='newest',

    # Save to CSV File
    with open('/home/w205/craigslist_scrape_tmp/scrape_temp.csv', 'wt') as f:
        for result in results: # had to use a '>' as a delimiter so the geotag doesn't get split up
            csv_line = str(result['datetime']) + '>' + \
                str(result['geotag']) + '>' + \
                str(result['has_image']) + '>' + \
                str(result['has_map']) + '>' + \
                str(result['id']) + '>' + \
                str(result['name']) + '>' + \
                str(result['price']) + '>' + \
                str(result['url']) + '>' + \
                str(result['where']) + '\n'
            f.write(csv_line)

scrape_craigslist()
