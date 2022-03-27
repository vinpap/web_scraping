import logging
import logging.handlers
import csv
import time
import threading
import os
from os import listdir
from os.path import isfile, join

from csvmanagerinterface import CSVManagerInterface


class CSVManager(CSVManagerInterface):
    
    """This module writes and manages the CSV files containing the job search results"""
    
    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log', maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)
        
        self.csvCleaner = threading.Thread(target=self.cleanOldCSVFiles)
        self.csvCleaner.start()
    
    def createCSV(self, offers, searchID):
        
        """offers: dictionary of job offers
        searchID: unique ID used to identify each CSV file and serve the
        right one when the user wants to download his search results"""
    
        filepath = "csv/" + str(searchID) + ".csv"
    
        with open(filepath, "w", newline="") as csvFile:
            
            fieldNames = ["Title", "URL", "Website", "Publication date"]
            offersWriter = csv.writer(csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            offersWriter.writerow(fieldNames)
            
            for i in offers:
                
                offersWriter.writerow([i[0], i[1], i[2], i[3]])
    
    def cleanOldCSVFiles(self):
        
        
            """This method regularly deletes all csv files older than 60 minutes"""
            
            while True:
            
                print("Deleting old CSV files...")
                
                
                path = "./csv"
                currentTime = time.time() * 1000
                
                filesList = [f for f in listdir(path) if isfile(join(path, f))]
                print(filesList)
                
                for i in filesList:
                    
                    if i.rfind(".csv"):
                    
                        print("Filename: " + i)
                        nameWithoutExtension = i[:-4]
                        fileDate = float(nameWithoutExtension)
                        
                        if currentTime - fileDate >= 3600000:
                            
                            os.remove(path + "/" + i)
                            print("File " + path + "/" + i + " deleted")
                
                time.sleep(3600)

            
        
 
          