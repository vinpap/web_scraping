import time
import pandas as pd
from snscrape.modules.twitter import TwitterSearchScraper

class Scraper:

    def __init__(self, format="", filename=""):

        self.supported_formats = ["csv"]
        if format in self.supported_formats:
            self.format = format
        else:
            print(f"WARNING: format {format} is not supported. Switching to display only")
            self.display_only = True
            return

        self.filename = filename
        if self.filename == "": self.display_only = True
        else: self.display_only = False



    def scrape(self, query="", results_count=0, language="en"):

        """query n'est utilisé que si cela a du sens pour le scraper en question.
        les résultats sont illimités si results_count = 0"""

        tweets_max_time = int(time.time()) - 604800

        search = query + " lang:" + language + " until_time:" + str(tweets_max_time)
        required_fields = ["id", "url", "date", "renderedContent", "hashtags", "replyCount", "retweetCount", "likeCount"]

        scraped_data = []
        tweets_processed = 0
        chunk_size = 10000

        while tweets_processed < results_count:
            scraping_results = TwitterSearchScraper(search).get_items()
            while tweets_processed < results_count:
                try:
                    tweet = next(scraping_results)
                    tweet.renderedContent = '''%s''' % tweet.renderedContent
                    if tweet.hashtags:
                        tweet.hashtags = str(tweet.hashtags).lstrip('[').rstrip(']')
                        tweet.hashtags = '''%s''' % tweet.hashtags

                except (TypeError, KeyError):
                    continue
                except StopIteration:
                    tweets_max_time -= 3000
                    search = query + " lang:" + language + " until_time:" + str(tweets_max_time)
                    break
                tweets_processed+=1
                if tweets_processed % 100 == 0:
                    print(str(tweets_processed) + " tweets scraped")
                scraped_data.append(tweet)
                if tweets_processed % chunk_size == 0:
                    print("Saving data chunk")
                    scraped_data = pd.DataFrame(scraped_data)[required_fields]
                    self.output(scraped_data)
                    scraped_data = []

        print("Final save")
        if scraped_data != []:
            scraped_data = pd.DataFrame(scraped_data)[required_fields]
            self.output(scraped_data)

    def output(self, scraped_data):

        """Ici, on enregistre ou affiche les résultats"""
        if self.display_only:
            print(scraped_data)

        elif self.format == "csv":
            scraped_data.to_csv(self.filename, index=False, mode='a', sep =',', escapechar=',')
