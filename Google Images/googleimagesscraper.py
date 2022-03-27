import os
import time
import io
import shutil
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from pyvirtualdisplay import Display
from PIL import Image
from datauri import DataURI, exceptions

class Google_images_scraper:

    """This class downloads images from Google Images, resize them according
    to the user's preferences and store them in a img_download folder."""

    def __init__(self):

        self.search_url = "https://www.google.com/"
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
            }
        self.download_path = "img_download/"


    def download_images(self, query, count=10, size=(200, 200)):

        """Request images matching the query string passed as a parameter.

        Parameters:
        * query: string containing the query requested by the user
        * count: number of images requested. Use get_image instead if you only
        want one. You might get a number of images below the count value if it is
        bigger than the number of available images on Google
        * size: tuple containing the dimensions we want the returned images to have

        The downloaded images will be stored in the img_download folder"""

        print(f"Downloading images for query {query}")

        display = Display(visible=0, size=(800, 600))
        display.start()

        # The line below only works for a Google Chrome web driver. You'll need to download Google Chrome as well
        # the web driver matching you version of Chrome in order for this to work.
        driver = webdriver.Chrome('./chromedriver')


        driver.set_window_size(1920, 1080)

        download_dir = self.download_path + query.replace(" ", "_")

        url = self.search_url + "search?q="+query+"&source=lnms&tbm=isch"
        driver.get(url)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        i = 1
        processed_images = 0
        missing_images_in_a_row = 0

        while processed_images < count:
            try:
                show_more_btn = driver.find_element_by_xpath("""//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input""")
                show_more_btn.click()
            except (NoSuchElementException, ElementNotInteractableException):
                pass

            xpath = """//*[@id="islrg"]/div[1]/div[""" + str(i) + """]/a[1]/div[1]/img"""
            try:
                img_tag = driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                missing_images_in_a_row += 1
                if missing_images_in_a_row > 10: break
                i += 1
                continue
            missing_images_in_a_row = 0
            img_url = img_tag.get_attribute('src')

            try:
                img = self.__download_from_data_uri(img_url)
            except exceptions.InvalidDataURI:

                try:
                    img = self.__download_from_http_url(img_url)

                except:
                    i += 1
                    continue

            img = img.resize(size)

            k = 1
            while os.path.exists(download_dir + "/" + f"{k}.png"): k += 1

            filename = f"{k}.png"
            filepath = download_dir + "/" + filename

            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            with open(filepath,'wb') as f:
                img.save(f)
            processed_images += 1
            i += 1

        print(f"DONE - downloaded {str(processed_images)}")


        driver.quit()


    def download_image(self, query, size=(200, 200)):
        """Call this if you only want to get one image"""
        self.get_images(query, 1, size)


    def __download_from_data_uri(self, uri):

        """Download an image from its data URI"""

        img_data_uri = DataURI(uri)
        return Image.open(io.BytesIO(img_data_uri.data))

    def __download_from_http_url(self, url):

        """Download an image from its HTTP URL"""

        r = requests.get(url, stream = True)
        if r.status_code == 200:
            return Image.open(io.BytesIO(r.content))
        else:
            raise
