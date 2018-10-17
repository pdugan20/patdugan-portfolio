import json
from google.appengine.api import urlfetch

DISCOGS_API = 'https://api.discogs.com/users/patdugan/collection/folders/0/releases'
API_KEY = 'qzhFhUTUMydigBFJCdGU'
API_SECRET = 'jVlHbmkHintWgTXXEIuENaNLwzoYoJwE'
PAGINATION_BASE = '150'

def record_collection():
    discogsUrl = DISCOGS_API
    discogsUrl += '?per_page=' + PAGINATION_BASE
    discogsUrl += '&key=' + API_KEY
    discogsUrl += '&secret=' + API_SECRET

    jsonRaw = urlfetch.fetch(discogsUrl)
    jsonObject = json.loads(jsonRaw.content)
    vinylCollection = jsonObject['releases']

    recordList = []

    for lp in vinylCollection:
        recordId = lp['id']
        recordName = lp['basic_information']['title']
        artistName = (lp['basic_information']['artists'][0]['name']).strip(' (2)')
        recordReleaseYear = lp['basic_information']['year'],
        albumArt = lp['basic_information']['thumb'],
        recordLabel = lp['basic_information']['labels'][0]['name'],
        recordUrl = 'http://www.discogs.com/release/' + str(recordId)
        recordReleaseYear = int(recordReleaseYear[0])

        currentRecord = [
            recordId,
            recordName,
            artistName,
            recordReleaseYear,
            recordUrl,
            albumArt[0],
            recordLabel[0]
        ]

        recordList.append(currentRecord)

    return recordList
