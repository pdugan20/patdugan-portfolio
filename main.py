import os
import urllib
import json
import jinja2
import webapp2

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')))

jinja_environment.trim_blocks = True
jinja_environment.lstrip_blocks = True
                    
class HomePage(webapp2.RequestHandler):
    def get(self):    
        path = jinja_environment.get_template('index.html')
        self.response.out.write(path.render())
    
class VinylPage(webapp2.RequestHandler):
    def get(self):        
        discogsUrl = 'https://api.discogs.com/users/patdugan/collection/folders/0/releases'
        
        paginationBase = '125'  
        consumerKey = 'qzhFhUTUMydigBFJCdGU'
        consumerSecret = 'jVlHbmkHintWgTXXEIuENaNLwzoYoJwE'
        
        discogsUrl += '?per_page=' + paginationBase
        discogsUrl += '&key=' + consumerKey
        discogsUrl += '&secret=' + consumerSecret
        
        vinylJsonRaw = urlfetch.fetch(discogsUrl)
        vinylJsonObject = json.loads(vinylJsonRaw.content)
        vinylCollection = vinylJsonObject['releases']
        
        recordCollection = []
        
        for lp in vinylCollection:
            recordId = lp['id']
            recordName = lp['basic_information']['title']
            artistName = lp['basic_information']['artists'][0]['name']
            recordReleaseYear = lp['basic_information']['year'],
            albumArt = lp['basic_information']['thumb'],
            recordLabel = lp['basic_information']['labels'][0]['name'],
            discogsUrl = 'http://www.discogs.com/release/' + str(recordId)
            recordReleaseYear = int(recordReleaseYear[0])
    
            currentRecord = [
                recordId,
                recordName,
                artistName,
                recordReleaseYear,
                discogsUrl,
                albumArt[0],
                recordLabel[0]
            ]   
      
            recordCollection.append(currentRecord)

        path = jinja_environment.get_template('index.html')
        self.response.out.write(path.render(template_values))

application = webapp2.WSGIApplication([
    ('/vinyl', VinylPage),
    ('/', HomePage)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
