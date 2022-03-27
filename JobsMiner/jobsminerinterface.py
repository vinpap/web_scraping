import abc

"""Interface for the jobs mining modules"""

from abc import ABC, abstractmethod

class JobsMinerInterface(ABC):

    @abstractmethod
    def findJob(self, jobSearch, ageLimit=False, resultsQueue=False):

        """jobSearch: dictionary object containing the keys "job", "location"
        and "country"
        ageLimit: optional parameter to limit the age of the job offers returned
        resultsQueue: queue where the results are stored"""
        
        pass


