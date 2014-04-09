import webapp2
import jinja2
import os
import logging

from google.appengine.api import urlfetch
from xml.etree import ElementTree as et

from helper import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class ArticleHandler(webapp2.RequestHandler):
    def get(self):
        myId = escapeAndFixId(self.request.get("id"))
        info = eval(find(myId))["response"]["docs"][0] # get the first doc (should only be one)
        del info['id'] # don't display id
        template_values = {}
        if "fsmImageUrl" in info:
            image_link = info["fsmImageUrl"][-1]
            del info['fsmImageUrl']
            template_values['picture_link'] = image_link
        else:
            teiUrl = info["fsmTeiUrl"][-1]
            del info['fsmTeiUrl']
            r = urlfetch.fetch(teiUrl).content
            xml = et.fromstring(r)
            text = xml.findall("text")[0]

            template_values['content'] = xmlToHTML(text)
        template_values['results'] = info
        template = jinja_environment.get_template("article.html")
        self.response.out.write(template.render(template_values))