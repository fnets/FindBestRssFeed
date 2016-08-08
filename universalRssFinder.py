#!/usr/local/bin/python

from google import search
from feedfinder2 import find_feeds
import feedparser
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import re
import requests


#Pre: inPodcastName is the name of the podcast that we want to get RSS URL for
#Post: A string of RSS URL
def findBestRssFeed(inPodcastName):
    assert (type(inPodcastName) is unicode), "findBestRssFeed: inPodcastName is not unicode"
    topProspects = getTopProspectiveRssHosts(inPodcastName, 3)

    rssCandidates = []

    #loading and sorting top prospective candidates from search
    for i in topProspects:
        candidates = loadAndFindRssUrlCandidates(i) #creates a list of tuples of scored candidates
        for item in candidates: #adds candidates list to rssCandidates list
            rssCandidates.append(item)

#Finalize RSS URL by verifying it
for i in rssCandidates:
    parsedCandidate = feedparser.parse(i[0])
        try:
            feedTitle = parsedCandidate.feed.title
                if feedTitle.lower() == inPodcastName.lower():
                    assert (type(i[0]) is unicode), "findBestRssFeed: " + i[0] +"is not unicode"
                        return i[0]
                    except AttributeError:
                        print i[0]+ ' has no feedtitle'
                            return None

print inPodcastName + ' has no correct candidates'
    return None


####################################
#FUNCTIONS CALLED IN findBestRssFeed
####################################

#Pre: inPodcastName is the exact name of the podcast
#Post: Returns inN number of top proscpective host page URLs for given podcast
#	   Returns a list of size inN or less
def getTopProspectiveRssHosts(inPodcastName, inN):
    assert (type(inPodcastName) is unicode), "getTopProspectiveRssHosts: inPodcastName is not String"
        assert (type(inN) is int), "getTopProspectiveRssHosts: inN is not int"

            #Notes: A function that takes in a phrase and returns the top n Google hits: https://pypi.python.org/pypi/googlesearch/ , https://pypi.python.org/pypi/google
            #feedparser and feedparser2 added.  Both work great, but might consider finding lxml or scrapy solution, for channel searching purposes, or for name scraping purposes
            search_results = []

                f = search( '"' + inPodcastName + '"' + 'podcast rss')
                    #creates a generator object that searches for inPodcastName in google
                    #and returns next URL of results

                    for x in xrange(inN):
                        search_results.append(f.next()) #stores next Google results

                            return search_results

#Pre: string of url found in google search for rss urls
#Post: List of tuples each with the following format: (outCandidateRssUrl,outCandidateScore)
def loadAndFindRssUrlCandidates(inProspectiveRssHostPageUrl):
    #load URL(inProspectiveRssHostPageUrl), search for potential RSS URLs on loaded URL, and score based on link existance and etc.
    assert (type(inProspectiveRssHostPageUrl[0]) is unicode), "loadAndFindRssUrlCandidates: inProspectiveRssHostPageUrl is not unicode"
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

                                                            scoredCandidates.append((rssCandidate, score))

                                                                assert (type(scoredCandidates[0]) is tuple), "loadAndFindRssUrlCandidates: scoredCandidates is not list of tuples"
                                                                    return scoredCandidates


#Pre: ioCandidateList is a list of tuples containing RSS URLs and score integers
def sortCandidatesByScore(ioCandidateList):
    #sorts ioCandidateList by score integers
    assert (type(ioCandidateList[0]) is tuple), "sortCandidatesByScore: ioCandidateList is not list of tuples"


    sorted_by_score = sorted(ioCandidateList, key=lambda tup: tup[0]) #Uses built-in Python sort method, defining the sorting key as the first value in the tuple

    return sorted_by_score


##############################################################
#FUNCTIONS CALLED IN TO SCRAPE STITCHER AND INPUT RSS INTO DB
##############################################################

#Pre: None, but eventually a string that indicates which podcatcher url to search
#Post: Tuple that contains podcast names and their respective categories
def getPodcastNames():
    #Searches through base URL for podcasts names and categories
    #currently only works for sitcher's site.
    #HTML PARSE MESSAGE DOES NOT COME FROM HERE

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
#for x in xrange():
#browser.get(base_url+category_links[x])
browser.get(base_url)
    print "only getting base URL for testing brevity"

    podcast_table = soup.findAll("span", {"class": "sl-showName"}) #All podcast names are stored with this class name in a dynamically created table
    category_table = soup.findAll("span", {"class": "sl-category"})  #All categories for podcasts found in previous line are stored with this class name in a dynamically created table

    for p in podcast_table:
        names.append(unicode(p.find('a').contents[0])) #pulls podcast names from link contents

    for p in category_table:
        categories.append(unicode(p.contents[0])) #pulls category names from link contents

###########################################################################
## TODO: NEED TO SEARCH FOR DUPLICATE ENTRIES                          ####
## MAY NOT NEED TO USE BASE URL, SINCE IT CONTAINS "BEST OF" PODCASTS  ####
###########################################################################

podcasts = zip(names, categories) #creates a list of tuples where each entry is (name, category)

    browser.close()

    assert (type(podcasts[1]) is tuple), "getPodcastNames: List is not tuples"
    assert (len(podcasts) >= 1), "getPodcastNames: List is empty"

    return podcasts



#Pre: Takes a 3-item list of podcast names, categories, and RSS URLs.
#Post: API Call for Postman Bookmark Submissions, containing podcast name, categories, and RSS URL for one podcast.
def submitBookmarks(inPodcastInfoList):
    #Submits podcast names, categories, and RSS URLs to NoSQL server using Postman API
    assert (type(inPodcastInfoList[0]) is unicode), "submitBookmarks: podcast[0] is not unicode"
    assert (type(inPodcastInfoList[1]) is unicode), "submitBookmarks: podcast[1] is not unicode"
    assert (type(inPodcastInfoList[2]) is unicode), "submitBookmarks: podcast[2] is not unicode"

    url = "https://tunr.soundspectrum.com//v1/bookmarks/" #API submission URL
    for podcast in inPodcastInfoList:
        title = podcast[0]
        category = podcast[1]
        rss_link = podcast[2]

        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n"+title+"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url_type\"\r\n\r\nP\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"categories\"\r\n\r\n"+category+"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"image\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n"+rss_link+"\r\n-----011000010111000001101001--"
        headers = {
            'content-type': "multipart/form-data; boundary=---011000010111000001101001",
            'authorization': "Token 1e71dfb93c8542561c4a2aa24c6ab81822562f27",
            'cache-control': "no-cache",
            'postman-token': "ba7cc2a8-6b11-f3b0-b132-26be0df1e9d7"
        }
        
        response = requests.request("POST", url, data=payload, headers=headers)
        assert ('csrf' not in response), "submitBookmarks: csrf rejected submission for" + title
    print 'Submissions complete.'


##############################################################
#MAIN FUNCTION
##############################################################



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
