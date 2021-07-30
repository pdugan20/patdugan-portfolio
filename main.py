import os
import jinja2
import webapp2
import lastfm
import discogs

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'template')
    )
)

jinja_environment.trim_blocks = True
jinja_environment.lstrip_blocks = True

template_values = {
    'app_version': os.environ.get('GAE_DEPLOYMENT_ID'),
}


class HomePage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('index.html')
        self.response.out.write(path.render(template_values))


class NewsletterPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('newsletter.html')
        self.response.out.write(path.render(template_values))


class HikearoundPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('hikearound.html')
        self.response.out.write(path.render(template_values))


class QuoraAdsManagerPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('quora_ads_manager.html')
        self.response.out.write(path.render(template_values))


class QuoraEmailsPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('quora_emails.html')
        self.response.out.write(path.render(template_values))


class QuoraMessagesPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('quora_messages.html')
        self.response.out.write(path.render(template_values))


class VinylPage(webapp2.RequestHandler):
    def get(self):
        page = self.request.get_all('page')

        if not page:
            page = 1
        else:
            page = page[0]

        discogsData = discogs.record_collection(page)
        artistData = lastfm.weekly_artists()

        template_values['record_collection'] = discogsData[0]
        template_values['pagination'] = discogsData[1]
        template_values['album_count'] = discogsData[1].get('items')
        template_values['artist_list'] = artistData

        path = jinja_environment.get_template('vinyl.html')
        self.response.out.write(path.render(template_values))


class ErrorPage(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        path = jinja_environment.get_template('error.html')
        self.response.out.write(path.render(template_values))


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/newsletter', NewsletterPage),
    ('/project/hikearound', HikearoundPage),
    ('/project/quora-ads-manager', QuoraAdsManagerPage),
    ('/project/quora-emails', QuoraEmailsPage),
    ('/project/quora-messages', QuoraMessagesPage),
    ('/vinyl', VinylPage),
    ('/.*', ErrorPage),
])
