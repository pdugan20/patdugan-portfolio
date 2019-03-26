import requests

DISCOGS_API = (
    'https://api.discogs.com/users/patdugan/collection/folders/0/releases'
)
DISCOGS_ALBUM_URL = 'http://www.discogs.com/release/'
API_KEY = 'qzhFhUTUMydigBFJCdGU'
API_SECRET = 'jVlHbmkHintWgTXXEIuENaNLwzoYoJwE'
ALBUMS_PER_PAGE = '150'


def record_collection():
    urlParameters = {
        'per_page': ALBUMS_PER_PAGE,
        'key': API_KEY,
        'secret': API_SECRET,
    }

    recordCollection = requests.get(
        DISCOGS_API, params=urlParameters
    ).json()['releases']

    recordList = []

    for lp in recordCollection:
        currentRecordInfo = {
            'id': lp['id'],
            'title': lp['basic_information']['title'],
            'artist': (
                lp['basic_information']['artists'][0]['name'].strip(' (2)')
            ),
            'year': lp['basic_information']['year'],
            'url': DISCOGS_ALBUM_URL + str(lp['id']),
        }
        recordList.append(currentRecordInfo)

    return recordList
