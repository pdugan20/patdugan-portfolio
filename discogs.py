import json
from google.appengine.api import urlfetch

DISCOGS_API = 'https://api.discogs.com/users/patdugan/collection/folders/0/releases'
DISCOGS_ALBUM_URL = 'http://www.discogs.com/release/'
API_KEY = 'qzhFhUTUMydigBFJCdGU'
API_SECRET = 'jVlHbmkHintWgTXXEIuENaNLwzoYoJwE'

def record_collection():
    discogsUrl = DISCOGS_API
    discogsUrl += '?per_page=' + '150'
    discogsUrl += '&key=' + API_KEY
    discogsUrl += '&secret=' + API_SECRET

    jsonRaw = urlfetch.fetch(discogsUrl)
    jsonObject = json.loads(jsonRaw.content)
    recordCollection = jsonObject['releases']

    recordList = []

    for lp in recordCollection:
        current_record_info = {
            'id': lp['id'],
            'title': lp['basic_information']['title'],
            'artist': lp['basic_information']['artists'][0]['name'].strip(' (2)'),
            'year': lp['basic_information']['year'],
            'url': DISCOGS_ALBUM_URL + str(lp['id']),
        }
        recordList.append(current_record_info)

    return recordList
