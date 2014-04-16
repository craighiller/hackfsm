from bottle import request, response, route, jinja2_template as template
from xml.etree import ElementTree as et
from google.appengine.api import urlfetch

import json
import re

@route('/find_snippets')
def snippetHandler():
    """
    Generates a snippet for an article where the snippet is ideally
    the first block of TEI that matches against the original query.
    This is used in conjunction with AJAX to populate the snippets
    on text search.
    Returns a json dictionary
    """
    query = request.query['query']
    queryLower = query.lower()
    teiUrl = request.query["fsmTeiUrl"]
    r = urlfetch.fetch(teiUrl).content
    xml = et.fromstring(r)
    text = xml.findall("text")[0] # ignore the header

    def acquireTarget(xmlNode):
        """
        Gets a snippet for a target from the XML
        """
        if xmlNode.text and xmlNode.text.lower().find(queryLower) != -1:
            return xmlNode.text
        temp = None
        for child in xmlNode:
            if not temp:
                temp = acquireTarget(child)
        if xmlNode.tail and xmlNode.tail.lower().find(queryLower) != -1:
            return xmlNode.tail
        return temp

    target = acquireTarget(text)

    response.add_header('content-type', 'application/json')

    if target:
        # use the first match and highlight it

        # use regex to match it so we can ignore case.
        subbedTarget = re.sub(query, "<mark>" + query + "</mark>", target, flags=re.IGNORECASE)
        count = r.lower().count(queryLower) # find number of times query appears in the response
        myResponse = {'snippet':subbedTarget, 'matches':count}
        return json.dumps(myResponse)
    else:
        # there were no pure matches.  Just get something so the user has a snippet
        def acquireEasterEgg(egg):
            """
            Gets the first word block in the TEI text that seems reasonable
            """
            if egg.text and len(egg.text.strip()) > 20: # make sure we don't get something short
                return egg.text
            temp = None
            for chicken in egg:
                if not temp:
                    temp = acquireEasterEgg(chicken)
            return temp

        easterEgg = acquireEasterEgg(text)
        myResponse = {'snippet':easterEgg, 'matches':0}
        return json.dumps(myResponse)
