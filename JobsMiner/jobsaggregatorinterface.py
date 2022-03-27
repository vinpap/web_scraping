import abc

"""Interface for the jobs aggregation module"""

from abc import ABC, abstractmethod

class JobsAggregatorInterface(ABC):

    @abstractmethod
    def findJob(self, jobSearch, searchID, ageLimit=False):

        """jobSearch: dictionary object containing the keys "job", "location"
        and "country"
        searchID: unique ID to identify the search. Used to associate a search
        with a CSV file
        ageLimit (optional): the age limit the user wants to apply in his 
        search"""
        pass



