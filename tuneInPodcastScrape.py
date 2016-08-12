import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import re

#Pre: None, but eventually a string that indicates which podcatcher url to search
#Post: Tuple that contains podcast names and their respective categories
def tuneinPodcastScrape(inScraperID):
 #Searches through base URL for podcasts names and categories
 #currently only works for sitcher's site.
 
    catDict = { #change these to category URLs
            'Comedy': 18,
            'Business': 14,
            'News & Politics': 41,
            'Society & Culture': 13,
            'Education': 27,
            'Entertainment': 52,
            'Games & Hobbies': 30,
            'Lifestyle & Health': 11,
            'Music & Commentary': 39,
            'Kids & Family': 55,
            'Science & Medicine': 48,
            'Religion & Spirituality': 47,
            'Sports':49,
            'Technology': 48,
            'International':41,
            'Storytelling': 13,
            'Pop Culture, TV & Film': 52,
          }
    base_url = u'http://tunein.com/radio/'
    home = u'Podcasts-c100000088/'
    html_source = scrapeSource(base_url+home)

    soup = BeautifulSoup(html_source, "html.parser") #allows for parsing and searching of HTML of page

    category_links = [u''] #adds a blank space for base URL search
    names = []
    categories = []

    category_table = soup.find_all('ul',{'class' : "column"}) #pulls the category list out of the HTML
    category_link_table = category_table[0].find_all('a',{'class' : "overlay-hover-trigger"}) #pulls the category list out of the HTML
    for entry in category_link_table:
        entry_contents = entry.get('href') #goes through all 'a' tags and pulls the values for href (the URL suffixes)
        needed_entry_contents = re.match(r'(\/radio\/)(.*)', entry_contents) #groups the redundant '/stitcher-list/' and unique part of URL suffix
        category_links.append(needed_entry_contents.group(2)) #saves the unique portion of the category URL suffixes             
    
    names = []
    for x in xrange(len(category_links)):
        html_source = scrapeSource(base_url + category_links[x])
        soup = BeautifulSoup(html_source, "html.parser")
        show_table = soup.find_all('h3',{'class' : "title"})
        for x in xrange(len(show_table)):
            names.append(show_table[x].get_text())
    print names    
    '''for x in xrange(len(category_link_table)):
      print 'link: ' + category_link_table.contents[0]
    
     #searches through link tags and pulls the URL suffixes needed
      for entry in category_link_table:
        entry_contents = entry.get('href') #goes through all 'a' tags and pulls the values for href (the URL suffixes)
        needed_entry_contents = re.match(r'(\/stitcher\-list\/)(.*)', entry_contents) #groups the redundant '/stitcher-list/' and unique part of URL suffix
        category_links.append(needed_entry_contents.group(2)) #saves the unique portion of the category URL suffixes     
   
   blah = 1

   #z = codecs.open('podcast_names-2.txt', 'w', 'utf-8')

   #Cycles through each category, and pulls the podcast names and categories
   for x in xrange(len(category_links)):

     #if blah > 1:
     # break

     blah += 1 
     html_source = scrapeSource(base_url+category_links[x]) 
     
     soup = BeautifulSoup(html_source, "html.parser") #allows for parsing and searching of HTML of page

     podcast_table = soup.findAll("span", {"class": "sl-showName"}) #All podcast names are stored with this class name in a dynamically created table
     category_table = soup.findAll("span", {"class": "sl-category"})  #All categories for podcasts found in previous line are stored with this class name in a dynamically created table

     for p in podcast_table:
        names.append(unicode(p.find('a').contents[0])) #pulls podcast names from link contents

     for p in category_table:
        if catDict[p.contents[0]] != 0: #does not include family and children podcasts
          categories.append(unicode(catDict[p.contents[0]])) #pulls category names from link contents


   podcasts = zip(names, categories) #creates a list of tuples where each entry is (name, category)

   json.dump(podcasts, codecs.open('podcasts-stitcher.json', 'w', 'utf-8') )


   '''
    exit(0)

    assert (type(podcasts[1]) is tuple), "getPodcastNames: List is not tuples"
    assert (podcasts), "getPodcastNames: List is empty"

    return podcasts #After demo, return to categories returned, tooxs


def scrapeSource(url):
  browser = webdriver.Chrome()
  browser.get(url) #opens chrome browser to witdraw data
  html_source = browser.page_source #Maybe could be done with regex or etree, but this is much more elegant
  browser.close()

  return html_source

if __name__ == '__main__':
    tuneinPodcastScrape(sys.argv[1])

