#!/usr/local/bin/python

from google import search
from feedfinder2 import find_feeds
import feedparser
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import re
import requests






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
    
    browser = webdriver.Chrome()
    base_url = u'https://www.stitcher.com/stitcher-list/'
    
    browser.get(base_url) #opens firefox browser to witdraw data
    html_source = browser.page_source #Maybe could be done with regex or etree, but this is much more elegant
    
    soup = BeautifulSoup(html_source, "html.parser") #allows for parsing and searching of HTML of page
    
    category_table = soup.findAll(id = "category-nav") #pulls the category list out of the HTML
    category_link_table = category_table[0].findAll('a') #finds all link tags in the category table
    
    category_links = [u''] #adds a blank space for base URL search
    names = []
    categories = []
    
    #searches through link tags and pulls the URL suffixes needed
    for entry in category_link_table:
    	entry_contents = entry.get('href') #goes through all 'a' tags and pulls the values for href (the URL suffixes)
    	needed_entry_contents = re.match(r'(\/stitcher\-list\/)(.*)', entry_contents) #groups the redundant '/stitcher-list/' and unique part of URL suffix
    	category_links.append(needed_entry_contents.group(2)) #saves the unique portion of the category URL suffixes
    
    #Cycles through each category, and pulls the podcast names and categories
    for x in xrange(len(category_links)):
    	browser.get(base_url+category_links[x])
    	podcast_table = soup.findAll("span", {"class": "sl-showName"}) #All podcast names are stored with this class name in a dynamically created table
    	category_table = soup.findAll("span", {"class": "sl-category"})  #All categories for podcasts found in previous line are stored with this class name in a dynamically created table
    
    	for p in podcast_table:
    		names.append(p.find('a').contents[0]) #pulls podcast names from link contents
    	
    	for p in category_table:
    		categories.append(p.contents[0]) #pulls category names from link contents
    
    ###########################################################################
    ## TODO: NEED TO SEARCH FOR DUPLICATE ENTRIES                          ####
    ## MAY NOT NEED TO USE BASE URL, SINCE IT CONTAINS "BEST OF" PODCASTS  ####
    ###########################################################################
    	
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

    url = "https://tunr.soundspectrum.com//v1/bookmarks/" #API submission URL
    for podcast in inPodcastInfoList:
        title = podcast[0]
        rss_link = podcast[2]
        
        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n"+title+"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url_type\"\r\n\r\nP\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"categories\"\r\n\r\n15\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"image\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n"+rss_link+"\r\n-----011000010111000001101001--"
        headers = {
            'content-type': "multipart/form-data; boundary=---011000010111000001101001",
            'authorization': "Token 1e71dfb93c8542561c4a2aa24c6ab81822562f27",
            'cache-control': "no-cache",
            'postman-token': "ba7cc2a8-6b11-f3b0-b132-26be0df1e9d7"
            }
        
        response = requests.request("POST", url, data=payload, headers=headers)




#Pre: Takes string that contains string that indicates intended podcatcher site to scrape
#Post: Completion message and a string of names, categories and RSS URLS Podcasts Added
def main(inPodcatcher):
    #calls all the functions that we have created
    
    
    if inPodcatcher == "stitcher":
        getPodcastNames()
    
    else:
        return inPodcatcher + "not available yet"
    
    return "Submissions complete."




    
if __name__ == '__main__':
    getPodcastNames() #Soon will be main

