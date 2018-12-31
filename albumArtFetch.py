import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup as bs

BASE_MB_SEARCH_URL = "https://musicbrainz.org/ws/2/release-group/?query="
BASE_CAA_SEARCH_URL = "https://coverartarchive.org/release-group/"

def getLinkToAlbumArt(artist, album, mbid = "", size="image"):
    #We are using coverartarchive.org API  
    #first, we need to find the album from musicbrainz.org
    #so we search the album and and get the mbid for the first result

	if not size in ["large", "small", "image"]:
		print("Invalid art size")
		return None
	
	if(len(mbid) == 0):#If we are not provided an mbid. Otherwise, skip the following. 
		print("attempting to get mbid")
		searchQuery = urllib.parse.quote_plus("%s %s" % (artist, album))#make search query http parsable 

		print("making musicbrainz request")
		response = urllib.request.urlopen(BASE_MB_SEARCH_URL+searchQuery) #Make HTTP request to database
		rawXML = response.read() #Store the XML formatted response in memory
		parsableXML = bs(rawXML,"xml") #Create BeautifulSoup Parsable XML

		results = parsableXML.find_all('release-group') #List of results. 
		#Will assume first result is correct unless user tells us otherwise. 
		
		try:
			mbid = results[0].get("id")
		except KeyError:
			print("Could not get mbid from first album result. Possible bad musicbrainz.org response")
			return None
			
	if(len(mbid) > 0):
		response = urllib.request.urlopen(BASE_CAA_SEARCH_URL+mbid)
		coverListingJSON = response.read()
		albumArtInfo = json.loads(coverListingJSON)
		"""for key in albumArtInfo:
			print(key)
			print(albumArtInfo[key])"""
			
	try:
		if size in ["large", "small"]:
			return albumArtInfo["images"][0]["thumbnails"][size]#Return the link to the album art using given size. 
		else: 
			return albumArtInfo["images"][0][size]
	except KeyError:
		print("Album art size '%s' not found in listing. Try another size" % size)
		return None
