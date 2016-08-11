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


    '''Tunr catID. worklistTuple
inFullWorklist = [
    ( 17, [             # Comedy - Performance
        ( "stitcher",  "subdir123/123" ),
        ( "stitcher",  "subdir123/859" ),
        ( "tunein",    "blah-223" ),
        ( "tunein",    "blah-224" ) ]
    ),
    ( 22, [             # Comedy - Discussion
        ( "stitcher",  "subdir/11" ),
        ( "tunein",    "blah-229" ) ]

    for i in inFullWorkList

        catID       = i[0]
        catWorkList = i[1]

        podcastNameDict = { }

         for j in catWorkList:
            scraperID  = j[0]
            scraperArg = j[1]
        '''

    if inPodcatcher == 'stitcher':
        podcastsAndCategories = universalRssFinder.scrapePodcastNames(inPodcatcher)

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
            g.write('Name: '+ str(podcastsAndCategoriesAndRssUrl[0])+ ' Category: '+str(podcastsAndCategoriesAndRssUrl[1])+' URL: '+ str(podcastsAndCategoriesAndRssUrl[2])+'\n')
            print rssURL
        g.close()

    for bookmark in podcastInfo:
        universalRssFinder.submitBookmarks(bookmark)

if __name__ == '__main__':
    testmain(sys.argv[1]) #Soon will be main