import time
import requests

LASTFM_API = 'http://ws.audioscrobbler.com/2.0/'
API_KEY = '83353938021dbe423e97d17e863ef498'
API_SECRET = 'f448a8da7f0f1d8d97ae9cfa6663b75d'
API_METHOD = 'user.getweeklyartistchart'


def weekly_artists():
    urlParameters = {
        'method': API_METHOD,
        'user': 'pdugan20',
        'from': str(time.time() - 1209600),  # 2 weeks
        'to': str(time.time()),
        'api_key': API_KEY,
        'format': 'json',
    }
    try:
        weeklyArtistChart = requests.get(
            LASTFM_API, params=urlParameters
        ).json()['weeklyartistchart']['artist']
    except:  # noqa
        return []

    artistList = []

    for artist in weeklyArtistChart:
        currentArtistInfo = {
            'name': artist['name'],
            'playcount': artist['playcount'],
            'url': artist['url'],
        }
        artistList.append(currentArtistInfo)

    return artistList[:5]
