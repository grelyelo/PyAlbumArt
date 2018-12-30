import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup as bs

BASE_MB_SEARCH_URL = "https://musicbrainz.org/ws/2/release-group/?query="
BASE_CAA_SEARCH_URL = "https://coverartarchive.org/release-group/"

def getLinkToAlbumArt(artist, album, mbid = ""):
    #We are using coverartarchive.org API  
    #first, we need to find the album from musicbrainz.org
    #so we search the album and and get the mbid for the first result

    
    if(len(mbid) > 0):
        #If provided a specific mbid, we can skip the search function and simply download the image. 
        coverListingJSON = urllib.request.urlopen(BASE_CAA_SEARCH_URL+mbid).read()
        

   #Music Brainz ID number, which we will find using the search function
    searchQuery = urllib.parse.quote_plus("%s %s" % (artist, album))#make search query http parsable 
    searchURL = BASE_MB_SEARCH_URL+searchQuery

    response = urllib.request.urlopen(searchURL) #Make HTTP request to database
    resultsXML = response.read()                 #Store the XML formatted response in memory
    bsXML = bs(resultsXML,"xml") #Create BeautifulSoup Parsable XML

    results = bsXML.find_all('release-group') 
    firstResult = results[0]#It is most likely that the first result will be correct, so we will assume it is correct. 
        
