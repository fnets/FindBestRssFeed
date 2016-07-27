#!/usr/local/bin/python

from google import search

#Pre: inPodcastName is the exact name of the podcast
#Post: Returns inN number of top proscpective host page URLs for given podcast
#	   Returns a list of size inN or less
def getTopProspectiveRssHosts(inPodcastName, inN):
    #Notes: A function that takes in a phrase and returns the top n Google hits: https://pypi.python.org/pypi/googlesearch/ , https://pypi.python.org/pypi/google
    search_results = []
    
    f = search(inPodcastName) #creates a generator object that searches for inPodcastName in google and returns next URL of results
    for x in xrange(inN):
        searchResults[x] = f.next() #stores next Google result
    
    return search_results

#Post: List of tuples each with the following format: (outCandidateRssUrl,outCandidateScore)
def loadAndFindRssUrlCandidates(inProspectiveRssHostPageUrl):
    #load URL(inProspectiveRssHostPageUrl), search for potential RSS URLs on loaded URL, and score based on link existance and etc.


#Pre: ioCandidateList is a list of tuples containing RSS URLs and score integers
def sortCandidatesByScore(ioCandidateList):
    #sorts ioCandidateList by score integers
    
    sorted_by_score = sorted(ioCandidateList, key=lambda tup: tup[0]) #Uses built-in Python sort method, defining the sorting key as the first value in the tuple
    
    return sorted_by_score

#Post: Returns a list of dictionaries corresponding to each channel in given RSS URL (channel and feed are pretty much interchangable.  sometimes there is more than one channel in a feed, but I've never seen it.)
def fetchRssChannels(inRssUrl):
    #locate and return RSS channels

#Pre: inPodcastName is the name of the podcast that we want to get RSS URL for
#Post: A tuple with the following fields: (rssUrl, dictContainingRssInfo)
def findBestRssFeed(inPodcastName)
    topProspects = getTopProspectiveRssHosts(inPodcastName, 3)

    rssCandidates = []
    
    #loading and sorting top prospective candidates from search
    for i in topProspects:
        candidates = loadAndFindRssUrlCandidates(i)
        rssCandidates.extend(candidates) #adds candidates list to rssCandidates list
    sortCandidatesByScore(rssCandidates)

    #Finalize RSS URL by verifying it
    for i in rssCandidates:
        channelList = fetchRssChannels(i)
        for j in channelList:
            if j['title'] == inPodcastName:
                return (i, j)

    return None




