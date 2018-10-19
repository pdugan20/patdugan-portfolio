import json
import time
from google.appengine.api import urlfetch

LASTFM_API = 'http://ws.audioscrobbler.com/2.0/'
API_KEY = '83353938021dbe423e97d17e863ef498'
API_SECRET = 'f448a8da7f0f1d8d97ae9cfa6663b75d'
API_METHOD = 'user.getweeklyartistchart'

def weekly_artists():
    lastFmUrl = LASTFM_API
    lastFmUrl += '?method=' + API_METHOD
    lastFmUrl += '&user=' + 'pdugan20'
    lastFmUrl += '&from=' + str(time.time() - 1209600) # 2 weeks
    lastFmUrl += '&to=' + str(time.time())
    lastFmUrl += '&api_key=' + API_KEY
    lastFmUrl += '&format=' + 'json'

    jsonRaw = urlfetch.fetch(lastFmUrl)
    jsonObject = json.loads(jsonRaw.content)
    weeklyArtistChart = jsonObject['weeklyartistchart']['artist']

    artistList = []

    for artist in weeklyArtistChart:
        current_artist_info = {
            'name': artist['name'],
            'playcount': artist['playcount'],
            'url': artist['url'],
        }
        artistList.append(current_artist_info)

    return artistList[:5]
