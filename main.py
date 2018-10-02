import os
import jinja2
import webapp2
import vinyl

from google.appengine.ext.webapp.util import run_wsgi_app

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'template')))

jinja_environment.trim_blocks = True
jinja_environment.lstrip_blocks = True

class HomePage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('index.html')
        self.response.out.write(path.render())

class QuoraMessagesPage(webapp2.RequestHandler):
    def get(self):
        path = jinja_environment.get_template('quora_messages.html')
        self.response.out.write(path.render())

application = webapp2.WSGIApplication([
    ('/vinyl', vinyl.VinylPage),
    ('/project/quora-messages', QuoraMessagesPage),
    ('/', HomePage)
])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
