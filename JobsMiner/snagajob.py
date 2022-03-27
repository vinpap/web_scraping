import logging
import logging.handlers
import re
import time


import requests
import requests.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


from jobsminerinterface import JobsMinerInterface


# The headers below are used to fake a browser and bypass protections against web crawling
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}



class Snagajob(JobsMinerInterface):

    """This class extracts data from job offers on snagajob.com (US)."""

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log', maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)

        self.supportedCountries = ("US")

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

        self.logger.debug("Search submitted with the following parameters: " + str(jobSearch) + str(ageLimit))


        startTime = time.time() # for development only, to be removed

        if jobSearch["country"] not in self.supportedCountries:

            resultsQueue.put("COUNTRY_NOT_SUPPORTED")
            return

        # a dictionary of crawled job offers
        jobs = {}


        searchURL = "https://www.snagajob.com/search?q=" + jobSearch["job"] + "&w=" + jobSearch["location"] + "&radius=5&sort=date"

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



        def retryLoading():

            """ This function is called when the infinite loader at the bottom
            of the page is still loading, i.e. when the new results are still
            loading """

            tries = 0

            while True:

                try:

                    self.driver.execute_script("document.getElementsByClassName('jobs')[0].scrollTop = document.getElementsByClassName('jobs')[0].scrollHeight - document.getElementsByClassName('jobs')[0].clientHeight;")
                    self.driver.find_element_by_css_selector('div.loader')
                    return True

                except NoSuchElementException:

                    tries+=1
                    self.driver.execute_script("document.getElementsByClassName('jobs')[0].scrollTop = document.getElementsByClassName('jobs')[0].scrollHeight - document.getElementsByClassName('jobs')[0].clientHeight;")

                    if tries >= 30:

                        return False

                    time.sleep(0.1)


        while True:

            try:



                self.driver.execute_script("document.getElementsByClassName('jobs')[0].scrollTop = document.getElementsByClassName('jobs')[0].scrollHeight - document.getElementsByClassName('jobs')[0].clientHeight;")


                self.driver.find_element_by_css_selector('div.loader')


            except NoSuchElementException:

                if not retryLoading():

                    break


        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        resultsTitles = soup.select("job-overview div.job-overview div.job-descr div.job h3")
        resultsLinks = soup.select("job-overview div.job-overview meta[itemprop='url']")
        resultsDates = []

        allOffersParsed = False

        for i in range(1, len(resultsTitles)+1):

            if allOffersParsed:

                break

            detailsLoaded = False

            self.driver.find_element_by_css_selector("job-overview[id='job-" + str(i) + "']").click()


            while not detailsLoaded:

                # Waiting for the job details on the right panel to be loaded

                try:

                    date = self.driver.find_element_by_css_selector("div.posting-days").text
                    date = self.convertAgeToInt(date, jobSearch["country"])
                    resultsDates.append(date)

                    if date > ageLimit:

                        # We stop opening the job details if the age for the
                        # current offer exceeds the age limit. The results are
                        # sorted by date, so there is no need to go any further
                        # down

                        allOffersParsed = True
                        resultsTitles = resultsTitles[:i]
                        resultsLinks = resultsLinks[:i]

                    detailsLoaded = True

                except NoSuchElementException:

                    continue


        for (i, j, k) in zip(resultsLinks, resultsDates, resultsTitles):


            offerURL = i["content"]



            if k.text not in jobs:

                jobs[k.text] = [(offerURL, "Snagajob", j)]


            else:

                jobs[k.text].append((offerURL, "Snagajob", j))



        resultsQueue.put(jobs)
        self.logger.debug("Search completed with the following parameters: " + str(jobSearch))
        return


    def convertAgeToInt(self, age, country):

        if country == "US" or country=="UK":

            if age.find("today") != -1:

                return 1

        elif country == "FR":

            if age.find("aujourd'hui") != -1:

                return 0


        return int(re.search('[0-9]+', age).group())


    def close(self):


        self.driver.quit()
