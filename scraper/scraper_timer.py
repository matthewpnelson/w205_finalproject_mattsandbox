# Timer Script for Scraper
#!/usr/bin/python


#from scraper import do_scrape
#import settings
import time
import sys
import traceback
import subprocess

if __name__ == "__main__":
    while True:
        #print("{}: Starting scrape cycle".format(time.ctime()))
        print("****************START SCRAPE******************")
        try:
            subprocess.call("./scrape_craigslist.sh", shell=True)
            #scrape_craigslist(max_rent= None, min_rent = None, cat = 'apa') # adjust?
        except KeyboardInterrupt:
            print("Exiting....")
            sys.exit(1)
        except Exception as exc:
            print("Error with the scraping:", sys.exc_info()[0])
            traceback.print_exc()
        else:
            #print("{}: Successfully finished scraping".format(time.ctime()))
            print("******SUCCESSFULLY FINISHED SCRAPE**********")
        time.sleep(60*20) #Sleep Interval 20mins
