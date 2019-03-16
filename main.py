import os
import jinja2
import webapp2
import lastfm
import discogs

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
        template_values['record_collection'] = discogs.record_collection()
        template_values['artist_list'] = lastfm.weekly_artists()
        path = jinja_environment.get_template('vinyl.html')
        self.response.out.write(path.render(template_values))


class ErrorPage(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        path = jinja_environment.get_template('error.html')
        self.response.out.write(path.render(template_values))


application = webapp2.WSGIApplication([
    ('/vinyl', VinylPage),
    ('/project/quora-messages', QuoraMessagesPage),
    ('/project/quora-ads-manager', QuoraAdsManagerPage),
    ('/', HomePage),
    ('/.*', ErrorPage),
])
