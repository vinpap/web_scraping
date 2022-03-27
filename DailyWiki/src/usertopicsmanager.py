import logging
import requests
import wikipedia

class UserTopicsManager:

    """This class is used to manage the operations related to the user's
    personalized topics: adding a new topic, removing one, or making sure the
    topics entered by the user match an existing category on Wikipedia"""

    def __init__(self, settings):

        self.logger = logging.getLogger(__name__)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)

        self.settings = settings

        self.max_topics_number = 10

    def insertNewTopic(self, topic):

        """The return value of that method is a string that can take these values:
            - "OK" if everything went well
            - "ALREADY EXISTS", if the topic entered by the user is already in the list
            - "TOO MANY TOPICS", if there are already too many topics"""
        

        result = ""

        if len(self.settings["TOPICS"]) >= self.max_topics_number:

            self.logger.debug("User tried to add a new topic, but the max number has already been reached") 

            return "TOO MANY TOPICS"

        if topic in self.settings["TOPICS"]:

            self.logger.debug("User tried to add a new topic, but it is already in the list")

            return "ALREADY EXISTS"


        self.logger.debug("Looking for " + "Category:" + str(topic))

        search_result = self.searchTopic(topic)

        if search_result=="OK":

            self.settings["TOPICS"].append(topic)

        return search_result
            

    def deleteTopic(self, topic):


        self.settings["TOPICS"].remove(topic)


    def searchTopic(self, topic):

        """The return value of that method is a string that can take these values:
            - "OK" if everything went well
            - "NOT FOUND" if the category cannot be found on Wikipedia, and there isn't
            one with a similar name
            - "NO CONNECTION", for connection issues"""

        try:

            wikipedia.page("Category:" + str(topic))

        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):

            self.logger.debug("Category:" + str(topic) + " not found")
            return "NOT FOUND"

        except requests.exceptions.ConnectionError:

            self.logger.debug("Category:" + str(topic) + " not found: connection lost")
            return "NO CONNECTION"


        return "OK"
        
