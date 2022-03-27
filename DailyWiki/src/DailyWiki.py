"""This is the main script of the app"""

from gui import GuiCore
import logging
import random
import os
import platform
import urllib
import sys
import time

from articleselector import ArticleSelector
from settingsreader import SettingsReader
from settingswriter import SettingsWriter
from settingsstorage import SettingsStorage
from guisettings import GuiSettings
from setworkingdirectory import setWorkingDirectory


MINIMUM_LOGGING_LEVEL = "INFO"

# =============================================================================
# First we need to define the working directory (C:\\User\AppData\Local\DailyWiki)
# If this directory does not exist yet for this user, then we need to create it
# and copy all the files needed. See setworkingdirectory for more info
# =============================================================================


setWorkingDirectory()



def checkNetworkStatus():

# =============================================================================
# Here we try to get a response from Wikipedia. If the requests still fail
# after a fixed number of trials, we exit the program.
# =============================================================================
    tries = 0

    while tries <= 20:

        try:

            urllib.request.urlopen('https://www.wikipedia.org/')
            return True

        except urllib.error.URLError:

            time.sleep(120)
            tries += 1

    logger.info("Unable to reach Wikipedia, please check your Internet connection")
    return False


logging.basicConfig(level=os.environ.get("LOGLEVEL", MINIMUM_LOGGING_LEVEL),
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

logger = logging.getLogger(__name__)

# =============================================================================
# Main script (used to launch the app)
# =============================================================================


if not checkNetworkStatus():

    sys.exit()


random.seed() # The random module is used by different subsytems

# =============================================================================
# SettingsStorage: manages the physical storage of the settings
# SettingsReader: reads the settings via SettingsStorage
# SettingsWriter: saves the settings via SettingsStorage
# =============================================================================

conf = SettingsStorage()
read = SettingsReader(conf)
write = SettingsWriter(conf)


article_selector = ArticleSelector(read)
app = GuiCore(article_selector)
gui_settings = GuiSettings(read, write)
app.setSettingsGui(gui_settings)


app.run()
