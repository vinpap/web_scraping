import abc

"""Interface for the CSV management module"""

from abc import ABC, abstractmethod

class CSVManagerInterface(ABC):

    @abstractmethod
    def createCSV(self, offers, searchID):

        """offers: dictionary of job offers
        searchID: unique ID used to identify each CSV file and serve the
        right one when the user wants to download his search results"""
        pass


