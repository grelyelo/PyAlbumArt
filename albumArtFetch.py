import urllib.request
import urllib.parse
from bs4 import BeautifulSoup as bs

BASE_MB_SEARCH_URL = "https://musicbrainz.org/ws/2/release-group"

def fetchAlbumArt(artist, album):
    #We are using coverartarchive.org API  
    #first, we need to find the album from musicbrainz.org
    #so we search the album and and get the mbid for the first result

  

    mbid = "" #Music Brainz ID number, which we will find using the search function
    searchQuery = urllib.parse.quote_plus("%s %s" % (artist, album))#make search query http parsable 
    search_url = BASE_MB_SEARCH_URL+searchQuery
    response = urllib.request.openurl(search_url) #Make HTTP request to database
    results_xml = response.read()                 #Store the XML formatted response in memory
    
    #topResult = 
    
    
