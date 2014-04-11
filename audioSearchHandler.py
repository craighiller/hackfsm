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
        info = popup(q, int(collection))['results']
        template_values = {}
        template_values["response"] = info
        template_values["typeOfResource"] = "audio"
        template = jinja_environment.get_template("audio.html")
        self.response.out.write(template.render(template_values))
