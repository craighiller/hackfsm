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

        filterType = self.request.get_all("filterType")
        if 'other' in filterType: 
            # exclude what is not in the filterType
            exclusion = set(typesOfResourcesDict.keys()) - set(filterType)
            exclusion - set('other')
            if len(exclusion) != 0:
                q = appendToQuery(q, '-fsmTypeOfResource:' + " OR -fsmTypeOfResource:".join(exclusion))
        else: 
            # only collect what is checked
            if len(filterType) != 0:
                q = appendToQuery(q, 'fsmTypeOfResource:' + " OR fsmTypeOfResource:".join(filterType))
            else:
                # nothing checked, check all
                filterType = typesOfResourcesDict.keys()

        template_values = {}
        start = self.request.get("start", -1)
        print(self.request.query_string)
        print(start)
        if start == -1:
            # first time visiting the page
            # we need query parameters so that the page links at the bottom of search will look right
            template_values["queryParameters"] = self.request.query_string
            start = 1
        else:
            # parse off last query parameter which will be &start=??
            template_values["queryParameters"] = "&".join(self.request.query_string.split('&')[:-1])
        print(template_values["queryParameters"])
        print(self.request.query_string == template_values["queryParameters"])

        start = int(start) - 1
        rowsPerPage = 15
        startRow = start*rowsPerPage

        template_values["typeOfResource"] = typeOfResource

        results = query(q, startRow, rowsPerPage)

        template_values['types'] = typesOfResourcesDict
        template_values['filterType'] = filterType
        template = jinja_environment.get_template("search.html")
        template_values["query"] = cgi.escape(self.request.get("search"))
        template_values["numPages"] = results["response"]["numFound"] // rowsPerPage + 1
        template_values["response"] = results["response"]["docs"]
        self.response.out.write(template.render(template_values))