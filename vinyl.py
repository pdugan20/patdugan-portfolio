import os
import json
import jinja2
import webapp2

from google.appengine.api import urlfetch

CURRENT_APP_VERSION = os.environ['CURRENT_VERSION_ID'].split('.', 1)[1]

DISCOGS_API = 'https://api.discogs.com/users/patdugan/collection/folders/0/releases'
CONSUMER_KEY = 'qzhFhUTUMydigBFJCdGU'
CONSUMER_SECRET = 'jVlHbmkHintWgTXXEIuENaNLwzoYoJwE'
PAGINATION_BASE = '150'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'template')))

jinja_environment.trim_blocks = True
jinja_environment.lstrip_blocks = True

class VinylPage(webapp2.RequestHandler):
    def get(self):
        discogsUrl = DISCOGS_API
        discogsUrl += '?per_page=' + PAGINATION_BASE
        discogsUrl += '&key=' + CONSUMER_KEY
        discogsUrl += '&secret=' + CONSUMER_SECRET

        vinylJsonRaw = urlfetch.fetch(discogsUrl)
        vinylJsonObject = json.loads(vinylJsonRaw.content)
        vinylCollection = vinylJsonObject['releases']

        recordCollection = []

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

            recordCollection.append(currentRecord)

        template_values = {
            'app_version': CURRENT_APP_VERSION,
            'record_collection': recordCollection,
        }

        path = jinja_environment.get_template('vinyl.html')
        self.response.out.write(path.render(template_values))
