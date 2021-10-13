#setlistAPIconnection.py
#https://api.setlist.fm/docs/1.0/index.html for header requirements and API guidelines. 

#This Python script connects to the setlist.fm API and pulls set list info for a specified band into one consolidated list. 

import json, requests, sys, time, os
from setlist_appid import appID

mbid = 'e01646f2-2a04-450d-8bf2-0d993082e058'           #Find the preferred artist MBID at https://musicbrainz.org/doc/MusicBrainz_Identifier. The band Phish is MBID 'e01646f2-2a04-450d-8bf2-0d993082e058'. 
totalPages = 2      #Each page has about 20 setlists. Phish has over 1900 sets (over 95 pages) so this can be very large for some artists. 
setlistFile = 'example.py'    #Input the .py filename to save the list of information. If no filepath given then the file will be located in the CWD.  

for page in range(1,totalPages+1):  #Cycle through each page in order. Most recent setlists are first.   
  count = 0                         #Keeping track of pages pulled for ending the combined setlists list. 
  url = 'https://api.setlist.fm/rest/1.0/artist/%s/setlists?p=%s' % (mbid, page)    #There are other possible URLs to pull additional data but this script only pulls setlist information. 
  
  header = {
  'Accept': 'application/json',     
  'x-api-key': appID,
  }
  
  response = requests.get(url, headers=header)
  response.raise_for_status()

  jsonMusicData = response.text                 #Per the header, the API gives JSON formatted information. You can change this but the script will need alteration as well. 
  pythonMusicData = json.loads(jsonMusicData)   #JSON module used to format the information for Python use.  

        #This writes each setlist.fm page to a .txt file for future use as a list of pages. If there are connectivity issues, this will act as a record of previously accessed pages. 
  count += 1
  with open(setlistFile, 'a', encoding="utf-8") as setFile:         #utf-8 encoding may not be required for every user/console, but it did for my windows 10 machine. 
    if count == 1:
      setFile.write('allPages = [')
    else:
      continue
    
    setFile.write(str(pythonMusicData) + ', ')      #you will need to manually open the .py list and close it with a ']'
    
  
  time.sleep(3)     #this may need tweaking depending on your internet connectivity to the setlist.fm API. 3 second wait time worked with 100mb/s. 
  
