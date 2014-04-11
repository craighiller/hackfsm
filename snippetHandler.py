import urllib2
from xml.etree import ElementTree as et
import json
import re

from bottle import request, response, route, TEMPLATE_PATH, jinja2_template as template

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
    r = urllib2.urlopen(teiUrl).read()
    xml = et.fromstring(r)
    text = xml.findall("text")[0] # ignore the header

    targets = []

    def acquireTargets(e):
        """
        Gets a list of all perfect matches in the TEI document with the
        query ignoring case.
        """
        if e.text and e.text.lower().find(queryLower) != -1:
            targets.append(e.text)
        for n in e:
            acquireTargets(n)
        if e.tail and e.tail.lower().find(queryLower) != -1:
            targets.append(e.tail)

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
        something = []
        def acquireSomething(e):
            """
            Gets the first word block in the TEI text that seems reasonable
            """
            if len(something): # we got something, halt the recursion
                return
            if e.text and len(e.text.strip()) > 20: # make sure we don't get something short
                something.append(e.text)
            for n in e:
                acquireSomething(n)

        acquireSomething(text)
        myResponse = {'snippet':something[0], 'matches':0}
        return json.dumps(myResponse)
