#!/usr/local/bin/python

from google import search
from feedfinder2 import find_feeds
import feedparser
from selenium import webdriver
from bs4 import BeautifulSoup
import sys






#Pre: inPodcastName is the exact name of the podcast
#Post: Returns inN number of top proscpective host page URLs for given podcast
#	   Returns a list of size inN or less
def getTopProspectiveRssHosts(inPodcastName, inN):
   print "getTopProspectiveRssHosts"
   #Notes: A function that takes in a phrase and returns the top n Google hits: https://pypi.python.org/pypi/googlesearch/ , https://pypi.python.org/pypi/google
   #feedparser and feedparser2 added.  Both work great, but might consider finding lxml or scrapy solution, for channel searching purposes, or for name scraping purposes
   search_results = []
   
   f = search( '"' + inPodcastName + '"' + 'podcast rss') 
   #creates a generator object that searches for inPodcastName in google 
   #and returns next URL of results
   
   for x in xrange(inN):
       search_results.append(f.next()) #stores next Google results

   return search_results








#Pre: Takes a base URL (stichter.com, TuneIn.com, etc.)
#Post: A list of tuples: (podcast name, and category)
def getPodcastNames():
    #Searches through base URL for podcasts names and categories
    #currently only works for sitcher's main list.
    print "getPodcastNames"
    browser = webdriver.Firefox()
    browser.get('https://www.stitcher.com/stitcher-list/') #opens firefox browser to witdraw data
    html_source = browser.page_source #Maybe could be done with regex or etree, but this is much more elegant
    
    soup = BeautifulSoup(html_source, "html.parser") #allows for parsing and searching of HTML of page
    
    podcast_table = soup.findAll("span", {"class": "sl-showName"}) #All podcast names are stored with this class name in a dynamically created table
    category_table = soup.findAll("span", {"class": "sl-category"})  #All categories for podcasts found in previous line are stored with this class name in a dynamically created table

    names = []
    for p in podcast_table:
    	names.append(p.find('a').contents[0])
    
    categories = []
    for p in category_table:
    	categories.append(p.contents[0])
    
    podcasts = zip(names, categories) #creates a list of tuples where each entry is (name, category)
    
    browser.close()
    
    return podcasts





#Post: List of tuples each with the following format: (outCandidateRssUrl,outCandidateScore)
def loadAndFindRssUrlCandidates(inProspectiveRssHostPageUrl):
   #load URL(inProspectiveRssHostPageUrl), search for potential RSS URLs on loaded URL, and score based on link existance and etc.
   print "loadAndFindRssUrlCandidates"
   scoredCandidates = []
   feeds = find_feeds(inProspectiveRssHostPageUrl) #returns list of RSS feeds found from input URL, through some reliable methods
   
   for rssCandidate in feeds:
       #assign score to feeds.  Use feedparser to find title and other info.  Remove points for SoundCloud, etc.

       if "itunes" not in rssCandidate:    
           parseRss = feedparser.parse(rssCandidate)
           score = 0
           rssKeyWords= ["feed", "rss", "atom", "xml"]
           
           if any(x in rssCandidate for x in rssKeyWords): 
               score += 1
               
               if parseRss.version != "":
                   score += 1
    
                   if "soundcloud" not in rssCandidate:
                      score += 1
    
           scoredCandidates.extend((score,rssCandidate))

   return rssCandidate




#Pre: ioCandidateList is a list of tuples containing RSS URLs and score integers
def sortCandidatesByScore(ioCandidateList):
    #sorts ioCandidateList by score integers
    print "sortCandidatesByScore"

    sorted_by_score = sorted(ioCandidateList, key=lambda tup: tup[0]) #Uses built-in Python sort method, defining the sorting key as the first value in the tuple

    return sorted_by_score
    
'''    
#Post: Returns a list of dictionaries corresponding to each channel in given RSS URL 
    #(channel and feed are pretty much interchangable.  sometimes there is more than one 
    #channel in a feed, but it only exists in RSS prior to v1.)
def fetchRssChannels(inRssUrl):
    #locate and return RSS channels
    meow
    #This dude was working on the same thing:   http://stackoverflow.com/questions/3362133/how-to-parse-rss-link-get-ulr-to-rss-from-the-page-in-python-framework-scrapy  
    
    #feedparser really struggles with this because it is dated, so going to investigate lxml and chilkat and 
        #future(https://wiki.python.org/moin/RssLibraries), but probably should move on to other working on other 
        #methods for now, because not really relevant'''




#Pre: inPodcastName is the name of the podcast that we want to get RSS URL for
#Post: A tuple with the following fields: (rssUrl, dictContainingRssInfo)
def findBestRssFeed(inPodcastName):
    print "findBestRssFeed"
    topProspects = getTopProspectiveRssHosts(inPodcastName, 3)

    rssCandidates = []
    
    #loading and sorting top prospective candidates from search
    for i in topProspects:
        candidates = loadAndFindRssUrlCandidates(i)
        rssCandidates.append(candidates) #adds candidates list to rssCandidates list
        # Currently, the above 1 line turns strings into array of chars
    rssCandidates = sortCandidatesByScore(rssCandidates)
    
    #Finalize RSS URL by verifying it
    for i in rssCandidates:
        parsedCandidate = feedparser.parse(i)
        if parsedCandidate.feed.title.lower() == inPodcastName.lower():
            return i

    return None





#Pre: Takes a 3-item list of podcast names, categories, and RSS URLs.
#Post: API Call for Postman Bookmark Submissions, containing podcast name, categories, and RSS URL for one podcast.
def submitBookmarks(inPodcastInfoList):
    #Submits podcast names, categories, and RSS URLs to NoSQL server using Postman API
    
    
    
    return "Submissions complete"





#Pre: Takes string that contains URL of intended podcatcher site to scrape as a string
#Post: Completion message and a string of names, categories and RSS URLS Podcasts Added
def main(inURL):
    #calls all the functions that we have created
    return "Submissions complete."




    
if __name__ == '__main__':
    getPodcastNames() #Soon will be main


1470416137998