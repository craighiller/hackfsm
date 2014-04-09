import webapp2
import jinja2
import os
import logging

from helper import appendToQuery, query
from xml.etree import ElementTree as et

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

import cgi

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("search")
        typeOfResource = self.request.get("type")
        if typeOfResource == "image":
            q = appendToQuery(q, '-fsmTeiUrl:[* TO *]') # don't show written text
        else:
            q = appendToQuery(q, '-fsmImageUrl:[* TO *]') # don't show images

        template_values = {}
        start = self.request.get("start", -1)
        rowsPerPage = 30
        if start == -1:
            template_values["queryParameters"] = self.request.query_string + "&start=1"
            start = 1
        else:
            template_values["queryParameters"] = self.request.query_string
        start = int(start) - 1
        startRow = start*rowsPerPage

        template_values["queryParameters"] = "&".join(template_values["queryParameters"].split('&')[:-1])
        template_values["typeOfResource"] = typeOfResource

        results = query(q, startRow)
        template = jinja_environment.get_template("search.html")
        template_values["header"] = results["responseHeader"]
        template_values["query"] = cgi.escape(self.request.get("search"))
        template_values["numPages"] = results["response"]["numFound"] // 30 + 1
        template_values["response"] = results["response"]["docs"]
        self.response.out.write(template.render(template_values))