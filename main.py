#!/usr/bin/env python

"""import webapp2
import jinja2
import os
import logging

from searchHandler import SearchHandler
from articleHandler import ArticleHandler
from snippetHandler import SnippetHandler
from audioHandler import AudioHandler
from audioSearchHandler import AudioSearchHandler
 
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template("home.html")
        self.response.out.write(template.render(template_values))
      
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/article', ArticleHandler),
    ('/find_snippets', SnippetHandler),
    ('/audioId', AudioHandler),
    ('/audioSearch', AudioSearchHandler)
], debug=True)"""

from bottle import route, run, jinja2_template as template

@route('/')
def main():
    return template("home.html")

run(host='localhost', port=8000, debug=True)

