import webapp2
import jinja2
import os
import logging

from google.appengine.api import urlfetch
from xml.etree import ElementTree as et

from helper import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AudioHandler(webapp2.RequestHandler):
    def get(self):
        myId = self.request.get("id")
        info = popupFindById(myId)['results'][0] # should only be one
        template_values = {}
        template_values["audioResult"] = info
        template_values["typeOfResource"] = "audio"
        for audioDict in info['audio_files']:
        	audioDict['transcript'] = 'hi'
        template = jinja_environment.get_template("article.html")
        self.response.out.write(template.render(template_values))
