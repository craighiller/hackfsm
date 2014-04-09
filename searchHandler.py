import webapp2
import jinja2
import os
import logging

from helper import appendToQuery, query, queryPluck
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

        typesOfResourcesList = queryPluck(q)['facet_counts']['facet_fields']['fsmTypeOfResource']
        typesOfResourcesDict = {'other':0}
        assert len(typesOfResourcesList) % 2 == 0
        for i in xrange(0, len(typesOfResourcesList), 2):
            if i >= 10:
                typesOfResourcesDict['other'] += typesOfResourcesList[i+1]
            else:
                typesOfResourcesDict[typesOfResourcesList[i]] = typesOfResourcesList[i+1]

        filter = self.request.get_all("filter")
        if 'other' in filter: 
            # exclude what is not in the filter
            exclusion = set(typesOfResourcesDict.keys()) - set(filter)
            exclusion - set('other')
            if len(exclusion) != 0:
                q = appendToQuery(q, '-fsmTypeOfResource:' + " OR -fsmTypeOfResource:".join(exclusion))
        else: 
            # only collect what is checked
            q = appendToQuery(q, '(fsmTypeOfResource:' + " OR fsmTypeOfResource:".join(filter) + ')')

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

        template_values['types'] = typesOfResourcesDict
        template_values['filter'] = filter
        template = jinja_environment.get_template("search.html")
        template_values["header"] = results["responseHeader"]
        template_values["query"] = cgi.escape(self.request.get("search"))
        template_values["numPages"] = results["response"]["numFound"] // 30 + 1
        template_values["response"] = results["response"]["docs"]
        self.response.out.write(template.render(template_values))