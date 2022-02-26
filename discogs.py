import requests

DISCOGS_API = (
    'https://api.discogs.com/users/patdugan/collection/folders/0/releases'
)
DISCOGS_ALBUM_URL = 'http://www.discogs.com/release/'
API_KEY = 'qzhFhUTUMydigBFJCdGU'
API_SECRET = 'jVlHbmkHintWgTXXEIuENaNLwzoYoJwE'
ALBUMS_PER_PAGE = '48'


def record_collection(page):
    urlParameters = {
        'page': page,
        'per_page': ALBUMS_PER_PAGE,
        'key': API_KEY,
        'secret': API_SECRET,
    }

    api = requests.get(
        DISCOGS_API, params=urlParameters
    ).json()

    recordCollection = api['releases']
    pagination = api['pagination']

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

    return [recordList, pagination]
