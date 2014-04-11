import jinja2
import os
import logging

from xml.etree import ElementTree as et

from helper import *

from bottle import get, route, run, TEMPLATE_PATH, jinja2_template as template

@route('/audioSearch')
def audioSearchHandler():
    return template("search.html")

"""
class AudioSearchHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("q")
        if not q:
            q = "[* TO *]" # collect all
        collection = self.request.get("collection")
        if not collection:
            collection = 1712
        else:
            collection = int(collection)
        results = popup(q, collection)
        if 'results' in results.keys():
            info = results['results']
        else:
            info = ""
        template_values = {}
        template_values["response"] = info
        template_values["collection"] = collection
        template_values["typeOfResource"] = "audio"
        template_values["numPages"] = 1
        template_values["query"] = self.request.get("q")
        template = jinja_environment.get_template("search.html")
        self.response.out.write(template.render(template_values))
        """
