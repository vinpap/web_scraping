from queue import Queue
from queue import Empty

from indeed import Indeed
from linkedin import Linkedin
from snagajob import Snagajob


#indeedMiner = Indeed()
linkedinMiner = Linkedin()
#snagajobMiner = Snagajob()

testSearches = {"botanist": ["Los Angeles", [4, 3, 0]],
                "developer": ["Atlanta", [1421, 1000, 10968]],
                "CEO": ["Portland", [3, 181, 28]],
                "driver": ["Chicago", [1000,1000, 7626]]}



jobSearch = {"job": "manager",
                 "location": "Dallas",
                 "country": "US"
            }

#def testIndeed():
#
#
#
#
#    resultsQueue = Queue()
#    offers = {}
#    jobNbrs = 0
#
#
#    indeedMiner.findJob(jobSearch, False, resultsQueue)
#
#    while True:
#
#        try :
#
#            result = resultsQueue.get_nowait()
#
#        except Empty:
#
#            break
#
#        if isinstance(result, dict):
#
#            for j in result:
#
#                if j not in offers:
#
#                    offers[j] = result[j]
#
#                    for k in result[j]:
#
#                        jobNbrs+=1
#
#                else:
#
#                    for k in result[j]:
#
#                        offers[j].append(k)
#                        jobNbrs+=1
#
#
#
#    assert jobNbrs == 1000, "Indeed - The number of results should be " + str(1000) + ", not " + str(jobNbrs)
#
#
#


def testLinkedin():

    resultsQueue = Queue()
    offers = {}
    jobNbrs = 0


    linkedinMiner.findJob(jobSearch, False, resultsQueue)

    while True:

        try :

            result = resultsQueue.get_nowait()

        except Empty:

            break

        if isinstance(result, dict):

            for j in result:

                if j not in offers:

                    offers[j] = result[j]

                    for k in result[j]:

                        jobNbrs+=1

                else:

                    for k in result[j]:

                        offers[j].append(k)
                        jobNbrs+=1



    assert jobNbrs == 1000, "Linkedin - The number of results should be " + str(1000) + ", not " + str(jobNbrs)

#def testSnagajob():
#
#
#    resultsQueue = Queue()
#    offers = {}
#    jobNbrs = 0
#
#
#    snagajobMiner.findJob(jobSearch, False, resultsQueue)
#
#    while True:
#
#        try :
#
#            result = resultsQueue.get_nowait()
#
#        except Empty:
#
#            break
#
#        if isinstance(result, dict):
#
#            for j in result:
#
#                if j not in offers:
#
#                    offers[j] = result[j]
#
#                    for k in result[j]:
#
#                        jobNbrs+=1
#
#                else:
#
#                    for k in result[j]:
#
#                        offers[j].append(k)
#                        jobNbrs+=1
#
#
#
#    assert jobNbrs == 9202, "Snagajob - The number of results should be " + str(9202) + ", not " + str(jobNbrs)
