import logging
import logging.handlers
import re

from bs4 import BeautifulSoup
import requests
import requests.exceptions


from jobsminerinterface import JobsMinerInterface


# The headers below are used to fake a browser and bypass the protections 
# against web crawling some websites use

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}



class Indeed(JobsMinerInterface):
    
    """This class extracts data from job offers on indeed.com (US) or indeed.fr (France)."""
    
    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log', maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)
        
        self.supportedCountries = ("US", "FR")
    
    def findJob(self, jobSearch, ageLimit=False, resultsQueue=False):
        
        """jobSearch: dictionary object containing the keys "job", "location"
        and "country"
        ageLimit: optional parameter to limit the age of the job offers returned
        resultsQueue: queue where the results are stored
        This method returns a dictionary of lists of tuples. Keys are job titles,
        and the tuples follow the format (URL, source site, age of the offer)"""
        
        self.logger.debug("Search submitted with the following parameters: " + str(jobSearch))

        
        if jobSearch["country"] not in self.supportedCountries:
            
            resultsQueue.put("COUNTRY_NOT_SUPPORTED")
            return 
        
        # a dictionary of crawled job offers
        jobs = {} 
        
        
        endOfResults = False
        
        if jobSearch["country"] == "US":
            
            searchURL = "https://www.indeed.com/jobs?q=" + jobSearch["job"] + "&l=" + jobSearch["location"] + "&sort=date"
        
        elif jobSearch["country"] == "FR":
            
            searchURL = "https://www.indeed.fr/emplois?q=" + jobSearch["job"] + "&l=" + jobSearch["location"]
        
    
        while not endOfResults:
            
            try:
            
                r = requests.get(searchURL, headers=headers)
            
            except requests.exceptions.HTTPError:
                
                self.logger.error("An HTTP error occured while sending a request to " + searchURL)
                
                resultsQueue.put("CONNECTION_ERROR")
                return 

            
            if r.status_code == 403:
                
                self.logger.error("Error 403: access denied while sending a request to " + searchURL)
                
                
                resultsQueue.put("ACCESS_DENIED")
                return 

            
            if r.status_code == 404:
                
                self.logger.error("Error 404: page not found while sending a request to " + searchURL)
                
                resultsQueue.put("PAGE_NOT_FOUND")
                return 

            
            self.logger.debug("Request sent to " + searchURL)
            
        
            soup = BeautifulSoup(r.content, "html.parser")
            
            searchResults = soup.select("div.jobsearch-SerpJobCard.unifiedRow.row.result h2 a")
            resultsDates = soup.select("span.date")
            
            for (i, j) in zip(searchResults, resultsDates):

                offerAge = j.string
                offerAge = self.convertAgeToInt(offerAge, jobSearch["country"])
                
                if ageLimit and offerAge > ageLimit:
                    
                    endOfResults = True
                    continue
                
                if jobSearch["country"] == "US":
                    
                    offerURL = "https://www.indeed.com" + i["href"]
                    
                
                elif jobSearch["country"] == "FR":
                
                    offerURL = "https://www.indeed.fr" + i["href"]
                
                
                
                if i["title"] not in jobs:
                                        
                    jobs[i["title"]] = [(offerURL, "Indeed", offerAge)]
                    
                
                else:
                    
                    offerAlreadyScraped = False
                    
                    # The loop below is used to make sure there are no duplicates
                    
                    for k in jobs[i["title"]]:
                        
                        if offerURL in k:
                            
                            offerAlreadyScraped = True
                            break
                    
                    if not offerAlreadyScraped : jobs[i["title"]].append((offerURL, "Indeed", offerAge))
            
            
            if jobSearch["country"] == "US":
                
                nextPage = soup.find("a", attrs={"aria-label":"Next"})
                
            elif jobSearch["country"] == "FR":
            
                nextPage = soup.find("a", attrs={"aria-label":"Suivant"})
            
            
            
            if nextPage: # If the tag above has not been found, it means that this was the last page of results
                
               
                
                if jobSearch["country"] == "US":
                    
                    searchURL = "https://www.indeed.com" + nextPage["href"]
                    
                elif jobSearch["country"] == "FR":
                
                    searchURL = "https://www.indeed.fr" + nextPage["href"]
                    
                continue
            
            else:
                
                endOfResults = True
            
        
        resultsQueue.put(jobs)
        self.logger.debug("Search completed with the following parameters: " + str(jobSearch))
        return 

    
    def convertAgeToInt(self, age, country):
        
        if country == "US":
            
            if age == "Today" or age == "Just posted":
                
                return 0
            
        elif country == "FR":
            
            if age == "Aujourd'hui" or age == "Publiée à l'instant":
                
                return 0
        
        
        return int(re.search('[0-9]+', age).group())  
    

            