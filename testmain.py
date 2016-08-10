import sys
import universalRssFinder
import datetime

#Pre: Takes string that contains string that indicates intended podcatcher site to scrape
#Post: Submits names, categories and RSS URLS to Tunr DB and prints a list of names, categories and RSS URLS Podcasts Added
def testmain(inPodcatcher):
    #calls all the functions that we have created
    
    if inPodcatcher == "stitcher":
        podcastsAndCategories = universalRssFinder.getPodcastNames()

    else:
        print inPodcatcher + " not available yet"
        return
    
    podcastInfo = []
    for podcastEntry in podcastsAndCategories: 
        f = open('rss_found.txt', 'a')
        f.write('\n\n'+str(datetime.datetime.now()))

        rssURL = universalRssFinder.findBestRssFeed(podcastEntry[0])
        if rssURL != None:
            podcastsAndCategoriesAndRssUrl = zip(podcastEntry,(rssURL,))
            podcastInfo.append(podcastsAndCategoriesAndRssUrl)
            f.write('Name: '+ str(podcastEntry[0])+ ' URL: '+str(rssURL)+'\n')
            print rssURL
        f.close()

    for bookmark in podcastInfo:
        submitBookmarks(bookmark)

if __name__ == '__main__':
    testmain(sys.argv[1]) #Soon will be main