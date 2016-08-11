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
    '''
    #Create Worklist loop
    
    for i in inFullWorkList:
        catID      = i[0]
        scraperID  = i[1]
        scraperArg = i[2]
    
        # Add podcast names we don't yet know about to our aggregate podcast name dict
        if 1:
            podcastNameDict = dict()
            podcastNames = scrapePodcastNames( scraperID, scraperArg )
            TRU_assert( podcastNames, "Got zero podcast names for scrapePodcastNames( '%s', '%s' )" % ( scraperID, scraperArg ) )
            
            for k in podcastNames:
                if k in podcastNameDict:
                    print "Found podcast DUPE '%s' for scraper = '%s'" % ( k, scraperID )
                else:
                    print "Found podcast      '%s' for scraper = '%s'" % ( k, scraperID )
                    podcastNameDict[k] = None


    # At this point, podcastNameDict[] contains all the podcast names we plan to submit for our given Tunr category ID
    for j in podcastNameDict:
        g = open('rss_found.txt', 'a')
         
        rssURL = findBestRssFeed( j )
        if rssURL == None:
            TRU_assert( False, "Failed to get a rss url for podcast '%s'" % j )
        else:
            podcastNameDict[j] = rssURL
            podcastsAndCategoriesAndRssUrl = podcastEntry +(rssURL,)
            podcastInfo.append(podcastsAndCategoriesAndRssUrl)
            g.write('Name: '+ str(podcastsAndCategoriesAndRssUrl[0])+ ' Category: '+str(podcastsAndCategoriesAndRssUrl[1])+' URL: '+ str(podcastsAndCategoriesAndRssUrl[2])+'\n')

    for j in podcastNameDict:
        submitBookmarks( catID, j, podcastNameDict[j] )

if __name__ == '__main__':
    testmain(sys.argv[1]) #Soon will be main