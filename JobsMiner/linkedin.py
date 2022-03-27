import logging
import logging.handlers
import random
import re
import time

import requests
import requests.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


from jobsminerinterface import JobsMinerInterface



# The headers below are used to fake a browser and bypass the protections
# against web crawling some websites use
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}




class Linkedin(JobsMinerInterface):

    """This class extracts data from linkedin.com (US & UK)
    or fr.linkedin.com (France)."""

    def __init__(self):


        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log', maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)


        self.supportedCountries = ("US", "FR", "UK")

        # The line below should be modified depending on the browser you use. You also need to download the right web webdriver
        # See Selenium's documentation for more information

        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.set_window_size(1920, 1080)


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


        if jobSearch["country"] == "US" or jobSearch["country"] == "UK":

            searchURL = "https://linkedin.com/jobs/search?keywords=" + jobSearch["job"] + "&location=" + jobSearch["location"] + "&sortBy=DD"

        elif jobSearch["country"] == "FR":

            searchURL = "https://fr.linkedin.com/jobs/search?keywords=" + jobSearch["job"] + "&location=" + jobSearch["location"] + "&sortBy=DD"



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

        self.driver.get(searchURL)

        self.logger.debug("Request sent to " + searchURL)

        try:

            self.driver.find_element_by_css_selector('div.no-results')
            self.logger.error("No results while sending a request to " + searchURL)
            resultsQueue.put("NO_RESULTS")
            return

        except NoSuchElementException:

            pass

        endOfResults = False
        clicksCounter = 0
        previousJobsCount = 0


        while not endOfResults and clicksCounter < 50:

            try:

                # If the element below is not found on the page, it means that
                # all results have not been displayed yet


                self.driver.find_element_by_css_selector('.inline-notification.see-more-jobs__viewed-all.hidden')


                try:

                    # Trying to find and click the "Show more" button


                    btn = self.driver.find_element_by_css_selector('button.infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible')
                    self.logger.debug("button found")
                    time.sleep(random.randint(500, 1100)/1000)


                    btn.click()
                    clicksCounter+=1


                except NoSuchElementException:

                    # If the button is not visible yet, it means that we must
                    # scroll down


                    self.driver.find_element_by_css_selector('body').send_keys(Keys.CONTROL, Keys.END)

                    time.sleep(random.randint(500, 1100)/1000)



                totalJobsCount = self.driver.find_element_by_css_selector(".results-context-header__job-count").text

                intsInString = re.findall('\d+', totalJobsCount)

                if len(intsInString) == 1:

                    totalJobsCount = int(intsInString[0])

                else:

                    totalJobsCount = int(intsInString[0] + intsInString[1])

                jobsDisplayed = len(self.driver.find_element_by_css_selector(".jobs-search__results-list").find_elements_by_css_selector(".result-card"))


                if (totalJobsCount <= jobsDisplayed) or (jobsDisplayed == previousJobsCount):

                    endOfResults = True

                previousJobsCount = jobsDisplayed


            except NoSuchElementException:

                endOfResults = True


        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        resultsTitles = soup.select("div.result-card__contents.job-result-card__contents h3.result-card__title.job-result-card__title")
        resultsLinks = soup.select("a.result-card__full-card-link")
        resultsDates = soup.select(".job-result-card__listdate") + soup.select(".job-result-card__listdate--new")



        for (i, j, k) in zip(resultsLinks, resultsDates, resultsTitles):

            offerAge = j.string
            offerAge = self.convertAgeToInt(offerAge, jobSearch["country"])

            if ageLimit and offerAge > ageLimit:

                continue



            offerURL = i["href"]



            if k.string not in jobs:

                jobs[k.string] = [(offerURL, "Linkedin", offerAge)]


            else:

                offerAlreadyScraped = False

                # The loop below is used to make sure there are no duplicates

                for l in jobs[k.string]:

                    if offerURL in l:

                        offerAlreadyScraped = True
                        break

                if not offerAlreadyScraped : jobs[k.string].append((offerURL, "Linkedin", offerAge))


        resultsQueue.put(jobs)
        self.logger.debug("Search completed with the following parameters: " + str(jobSearch))
        return


    def convertAgeToInt(self, age, country):

        if country == "US" or country=="UK":

            if age.find("minute") or age.find("hour"):

                return 0

            if age.find("week"):

                return int(re.search('[0-9]+', age).group()) * 7

        elif country == "FR":

            if age.find("minute") or age.find("heure"):

                return 0

            if age.find("semaine"):

                return int(re.search('[0-9]+', age).group()) * 7


        return int(re.search('[0-9]+', age).group())


    def close(self):

        self.driver.quit()
