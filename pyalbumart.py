import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup as bs

BASE_MB_SEARCH_URL = "https://musicbrainz.org/ws/2/release-group/?query="
BASE_CAA_SEARCH_URL = "https://coverartarchive.org/release-group/"

def getLinkToAlbumArt(artist, album, mbid = "", art="front"):
	
	#We are using coverartarchive.org API  
    #first, we need to find the album from musicbrainz.org
    #so we search the album and and get the mbid for the first result

	if(len(mbid) == 0):#If we are not provided an mbid, search for correct mbid.
		mbid = searchMusicbrainz(artist, album) 
			
	if(len(mbid) > 0):
		#If we have an MBID, we can try to search the cover art archive for the art. 
		caaHeadResponse = requests.head(BASE_CAA_SEARCH_URL+mbid+"/"+art, allow_redirects=True)
		return caaHeadResponse.url
	else:
		return None


def searchMusicbrainz(artist, album):#Try to search Musicbrainz.org for album. 
		artist=urllib.parse.quote_plus(artist)
		album=urllib.parse.quote_plus(album)
		searchQuery = "artist:"+artist+"%20AND%20release:"+album+"&limit=1"
                
        #Make the search
		response = urllib.request.urlopen(BASE_MB_SEARCH_URL+searchQuery) 
		
		rawXML = response.read() #Store the XML formatted response in memory
		parsableXML = bs(rawXML,"xml") #Create BeautifulSoup Parsable XML
		results = parsableXML.find_all('release-group') #List of results. 
		#Will assume first result is correct unless user tells us otherwise. 
		
		try:
			mbid = results[0].get("id")
			return mbid
		except KeyError:
			print("Could not get mbid from first album result. Possible bad musicbrainz.org response")
			return None
