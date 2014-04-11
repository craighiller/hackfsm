import webapp2
import jinja2
import os
import logging

from google.appengine.api import urlfetch
from xml.etree import ElementTree as et

from helper import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AudioSearchHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("q")
        if not q:
            q = "[* TO *]"
        collection = self.request.get("collection")
        if not collection:
            collection = 1712
        results = popup(q, int(collection))
        if 'results' in results.keys():
            info = results['results']
        else:
            info = ""
        template_values = {}
        template_values["response"] = info
        template_values["typeOfResource"] = "audio"
        template_values["numPages"] = 1
        template_values["query"] = self.request.get("q")
        template = jinja_environment.get_template("search.html")
        self.response.out.write(template.render(template_values))
