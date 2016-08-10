import sys
import universalRssFinder
import datetime

#Pre: Takes string that contains string that indicates intended podcatcher site to scrape
#Post: Submits names, categories and RSS URLS to Tunr DB and prints a list of names, categories and RSS URLS Podcasts Added
def testmain(inPodcatcher):
    #calls all the functions that we have created
    f = open('no_rss_found.txt', 'a')
    f.write('\n\n'+str(datetime.datetime.now())+'\n')
    f.close()
    g = open('rss_found.txt', 'a')
    g.write('\n\n'+str(datetime.datetime.now())+'\n')
    g.close()
    
    if inPodcatcher == "stitcher":
        podcastsAndCategories = universalRssFinder.getPodcastNames()

    else:
        print inPodcatcher + " not available yet"
        return
    
    podcastInfo = []
    for podcastEntry in podcastsAndCategories: 
        g = open('rss_found.txt', 'a')

        rssURL = universalRssFinder.findBestRssFeed(podcastEntry[0])
        if rssURL != None:
            podcastsAndCategoriesAndRssUrl = podcastEntry +(rssURL,)
            podcastInfo.append(podcastsAndCategoriesAndRssUrl)
            g.write('Name: '+ str(podcastInfo[0])+ ' Category: '+str(podcastInfo[1])+' URL: '+ str(podcastInfo[2])+'\n')
            print rssURL
        g.close()

    for bookmark in podcastInfo:
        universalRssFinder.submitBookmarks(bookmark)

if __name__ == '__main__':
    testmain(sys.argv[1]) #Soon will be main