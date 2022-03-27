
import time
from scraper import Scraper

test = Scraper("csv", "results.csv")
t1 = int(time.time())
test.scrape(results_count=1000000)
t2 = int(time.time())
print("Process finished in " + str(t2-t1) + " seconds")
