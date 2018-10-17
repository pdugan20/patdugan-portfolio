import os
import jinja2
import webapp2
import lastfm
import discogs

from google.appengine.ext.webapp.util import run_wsgi_app

CURRENT_APP_VERSION = os.environ['CURRENT_VERSION_ID'].split('.', 1)[1]

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'template')))

jinja_environment.trim_blocks = True
jinja_environment.lstrip_blocks = True

template_values = {
    'app_version': CURRENT_APP_VERSION,
}

class HomePage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('index.html')
        self.response.out.write(path.render(template_values))

class QuoraMessagesPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('quora_messages.html')
        self.response.out.write(path.render(template_values))

class QuoraAdsManagerPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('quora_ads_manager.html')
        self.response.out.write(path.render(template_values))

class VinylPage(webapp2.RequestHandler):
    def get(self):
        recordCollection = discogs.record_collection()
        artistList = lastfm.weekly_artists()
        template_values = {
            'app_version': CURRENT_APP_VERSION,
            'record_collection': recordCollection,
            'artist_list': artistList,
        }
        path = jinja_environment.get_template('vinyl.html')
        self.response.out.write(path.render(template_values))

application = webapp2.WSGIApplication([
    ('/vinyl', VinylPage),
    ('/project/quora-messages', QuoraMessagesPage),
    ('/project/quora-ads-manager', QuoraAdsManagerPage),
    ('/', HomePage)
])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
