from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
from bs4 import BeautifulSoup

def getPodcastNames():
   
    browser = webdriver.Chrome()
    base_url = u'https://www.shoutcast.com/'
    entries = []

    
    browser.get(base_url) #opens chrome browser to witdraw data
    '''
    browser.maximize_window()

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'down')))
    list_of_links = browser.find_elements_by_class_name("down")
    for link in list_of_links:
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'down')))
        # print link
        link.click()
        
        element = wait.until(EC.element_to_be_clickable((By.XPATH,".//*/a[@class='m3u']")))
        download = link.find_element_by_class_name("m3u")
        download.click()
        
        print download
              
        time.sleep(2)

        #link.click()
        
    browser.close()'''
    

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"m3u")))
    
    html_source = browser.page_source #Maybe could be done with regex or etree, but this is much more elegant

    soup = BeautifulSoup(html_source, "html.parser") #allows for parsing and searching of HTML of page
    
    station_list = soup.findAll('tr',id=True)
    for station in station_list:
        name = station.contents[2].get_text() #REPEATED CODE! Too tired to figure out a streamline right now.
        genre = station.contents[3].get_text()
        listeners = station.contents[4].get_text()
        bitrate = station.contents[5].get_text()
        encode = station.contents[6].get_text()
        
        m3u_link = station.find(class_='m3u').get('href')
        pls_link = station.find(class_='pls').get('href')
        xspf_link = station.find(class_='xspf').get('href')
        
        entry = {'name':name, 'genre':genre, 'listeners':listeners, 'bitrate':bitrate, 'encode':encode, 'm3u_link':m3u_link, 'pls_link':pls_link, 'xspf_link':xspf_link}
        entries.append(entry)
    
    json.dump( entries, open('shoutcast-masterList.json', 'w'), sort_keys=True, indent=4, separators=(',', ': ' ) )
        

    
    '''
    links.append(['m3u',m3u_links) #pulls the category list out of the HTML
    links.append(['pls',pls_links])
    
    for p in podcast_table:
        names.append(unicode(p.find('a').contents[0])) #pulls podcast names from link contents    
    
    category_link_table = category_table[0].findAll('a') #finds all link tags in the category table
    '''
    
    browser.close()
    
    '''
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
    ## TODO: NEED TO SEARCH FOR DUPLICATE ENTRIES                    ####
    ## MAY NOT NEED TO USE BASE URL, SINCE IT CONTAINS "BEST OF" PODCASTS  ####
    ###########################################################################

    podcasts = zip(names, categories) #creates a list of tuples where each entry is (name, category)

    browser.close()

    assert (type(podcasts[1]) is tuple), "getPodcastNames: List is not tuples"
    assert (podcasts), "getPodcastNames: List is empty"

    return podcasts'''


if __name__ == '__main__':
    getPodcastNames()