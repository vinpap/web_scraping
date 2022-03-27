import logging
import logging.handlers
import threading
from queue import Queue
from queue import Empty

from jobsaggregatorinterface import JobsAggregatorInterface
from csvmanager import CSVManager
from indeed import Indeed
from linkedin import Linkedin
from snagajob import Snagajob


class JobsAggregator(JobsAggregatorInterface):
    
    """This class instantiates and coordinates the different modules responsible 
    for carrying out the web scraping and generate the CSV. It also combines
    all the search results into a single dictionary"""
    
    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log', maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)
        
        self.csvManager = CSVManager()
    
    def findJob(self, jobSearch, searchID, ageLimit=False):
        
        """jobSearch: dictionar containing the keyx "job", "location" and "country"
        ageLimit: integral that defines the age after which the offers 
        should be ignored
        This method returns a list of tuples"""
        
        self.logger.debug("Search submitted with the following parameters: " + str(jobSearch))
        
        indeedMiner = Indeed()
        linkedinMiner = Linkedin()
        snagajobMiner = Snagajob()
        
        # Each jobs mining module is launched in a dedicated thread.
        # offersList is the list returned by this method. It contains tuples
        # resultsQueue is used by the different jobs mining module to store their 
        # search results
        
        offersList = [] 
        executionThreads = []
        resultsQueue = Queue() 
        
            
        executionThreads.append(threading.Thread(target=linkedinMiner.findJob, args=(jobSearch, ageLimit, resultsQueue)))
        executionThreads.append(threading.Thread(target=snagajobMiner.findJob, args=(jobSearch, ageLimit, resultsQueue)))
        executionThreads.append(threading.Thread(target=indeedMiner.findJob, args=(jobSearch, ageLimit, resultsQueue)))

            
        for i in executionThreads:
            
            i.start()
        
        for i in executionThreads:
            
            i.join()
        
        while True:
            
            try : 
                
                result = resultsQueue.get_nowait()
            
            except Empty:
            
                break
            
            # The mining modules must return dictionaries!
            
            if isinstance(result, dict):
                
                for j in result:
                    
                    for k in result[j]:
                            
                        offersList.append([j, k[0], k[1], k[2]])
                        
        self.sortJobs(offersList) # Offers are sorted by age
        
        for i in range(0, len(offersList)):
            
            # The age of the offers in the results is converted to string
            # for convenience
            
            offersList[i][3] = str(offersList[i][3])
#            
                    
        if len(offersList) != 0:

            self.csvManager.createCSV(offersList, searchID)
        
        self.logger.debug("Search completed with the following parameters: " + str(jobSearch))
        

        linkedinMiner.close()
        snagajobMiner.close()
            
        return offersList
    
    def sortJobs(self, offersList):
        
        def getAge(offer):
            
            return offer[3]
        
        offersList.sort(key=getAge)
    

        
        