from bottle import request, response, route, jinja2_template as template
from xml.etree import ElementTree as et

import urllib2
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
    xml = et.fromstring(urllib2.urlopen(teiUrl).read())
    text = xml.findall("text")[0] # ignore the header

    targets = []

    def acquireTargets(xmlNode):
        """
        Gets a list of all perfect matches in the TEI document with the
        query ignoring case.
        """
        if xmlNode.text and xmlNode.text.lower().find(queryLower) != -1:
            targets.append(xmlNode.text)
        for child in xmlNode:
            acquireTargets(child)
        if xmlNode.tail and xmlNode.tail.lower().find(queryLower) != -1:
            targets.append(xmlNode.tail)

    acquireTargets(text)

    response.add_header('content-type', 'application/json')

    if len(targets) != 0:
        # use the first match and highlight it
        target = targets[0]

        # use regex to match it so we can ignore case.
        subbedTarget = re.sub(query, "<mark>" + query + "</mark>", target, flags=re.IGNORECASE)

        myResponse = {'snippet':subbedTarget, 'matches':len(targets)}
        return json.dumps(myResponse)
    else:
        # there were no pure matches.  Just get something so the user has a snippet
        easterEgg = []
        def acquireEasterEgg(egg):
            """
            Gets the first word block in the TEI text that seems reasonable
            """
            if len(easterEgg): # we got something, halt the recursion
                return
            if egg.text and len(egg.text.strip()) > 20: # make sure we don't get something short
                easterEgg.append(egg.text)
            for chicken in egg:
                acquireEasterEgg(chicken)

        acquireEasterEgg(text)
        myResponse = {'snippet':easterEgg[0], 'matches':0}
        return json.dumps(myResponse)
