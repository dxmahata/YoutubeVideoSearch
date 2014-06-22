'''
Created on Jun 21, 2014

@author: Debanjan Mahata
'''
__author__ = "Debanjan Mahata"

import requests
import sys

#variable for the api key
YOUTUBE_API_KEY = ""

#base url for activity requests to google 
BASE_URL_YOUTUBE = "https://www.googleapis.com/youtube/v3/search"

#variable for tracking the number of requests to google server
API_REQUEST_COUNT = 0


def setApiKey():
    """It loads the API key from youtube_api.txt"""
    global YOUTUBE_API_KEY
    try:
        #reads the api key from the google_api.txt file
        fp = open("youtube_api.txt")
        YOUTUBE_API_KEY = fp.readline()
        if YOUTUBE_API_KEY == "":
            print("The youtube_api.txt file appears to be blank")
            print("If you do not have an API Key from GOOGLE, please register for one at: http://developers.google.com")
            sys.exit(0)
                
        fp.close()
    except IOError:
        print('API Key not found! Please create and fill up youtube_api.txt file in the same directory which contains the youtubeVideoSearch module')
        print('If you do not have an API Key from GOOGLE, please register for one at: http://developers.google.com')
        sys.exit(0)
    except Exception as e:
        print(e)
        



def defaultSearch(baseUrl,params):
    """function for searching the videos in the default mode as documented by the youtube api
    This function cannot get more that 50 videos at one time.
    
    INPUT -> 
        baseUrl : base url for getting youtube videos
        params : a dictionary of GET request parameters
    
    OUTPUT -> 
        response : returns the response returned by the google server as a python dictionary object
    """
    global API_REQUEST_COUNT 
    try:
        #GET request sent to google
        r = requests.get(baseUrl,params=params)
        API_REQUEST_COUNT +=1
        
        #response in json format converted into a dictionary
        response = eval(r.text)
        return response

    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }
    

def fullSearch(q,options={}):
    """function for iterating through the entire set of videos for a particular query. Not restricted to
    the default (50) set of videos returned in a single page. Uses the nextPageToken and requests for
    more videos.
    
    INPUT ->
        q : the search query
        options : a dictionary of options as provided by the youtube api .Please check here
                    https://developers.google.com/youtube/v3/docs/search/list
                    for the details of the various options available.
                    
    
    OUTPUT -> 
        response : returns a stream of videos
    """
    
    #dictionary for containing the GET query parameters.
    payload = {}
    #setting the query parameter
    payload["query"] = q
    #setting the youtube api key
    payload["key"] = YOUTUBE_API_KEY
    #setting the parameter for the number of returned results to 50
    payload["maxResults"] = 50
    #setting the order of the returned results to recent.
    payload["order"] = "date"
    #setting the part parameter as explained at https://developers.google.com/youtube/v3/getting-started to snippet
    payload["part"] = "snippet" 
    #setting the type parameter to video
    payload["type"] = "video"
    
    #setting the options if provided, the provided option overrides the default options set above.
    for option in options:
        payload[option] = options[option]

    
    #list for containing the activity items
    allItems = list([])
    
    #response for the first page
    resp = defaultSearch(BASE_URL_YOUTUBE,payload)
    
    #nextPageToken for looking for further activities
    nextPageToken = resp["nextPageToken"]
    allItems += resp["items"]
    
    while nextPageToken != "":
        #nextPageToken for looking for further activities
        nextPageToken = resp["nextPageToken"]
        
        #including nestPageToken in the parameters passed for the GET request
        payload["pageToken"] = nextPageToken
        resp = defaultSearch(BASE_URL_YOUTUBE,payload)
        allItems += resp["items"]
        for item in allItems:
            yield item
            

def search(q,options={}):
    """function for searching a stream of activities in Youtube related to a given query, with 
    suitable options.
    
    INPUT ->
        q : the search query
        options : a dictionary of options as provided by the youtube api .Please check here
                    https://developers.google.com/youtube/v3/docs/search/list
                    for the details of the various options available.
                    
    
    OUTPUT -> 
        response : returns a set of 50 activities

    """
    
    #dictionary for containing the GET query parameters.
    payload = {}
    #setting the query parameter
    payload["query"] = q
    #setting the youtube api key
    payload["key"] = YOUTUBE_API_KEY
    #setting the parameter for the number of returned results to 50
    payload["maxResults"] = 50
    #setting the order of the returned results to recent.
    payload["order"] = "date"
    #setting the part parameter as explained at https://developers.google.com/youtube/v3/getting-started to snippet
    payload["part"] = "snippet" 
    #setting the type parameter to video
    payload["type"] = "video"
    
    #setting the options if provided, the provided option overrides the default options set above.
    for option in options:
        payload[option] = options[option]
    
    #response for the default search
    resp = defaultSearch(BASE_URL_YOUTUBE,payload)
    return resp
        


