import urllib2
from xml.etree import ElementTree as et
import json
import re

from bottle import request, response, route, TEMPLATE_PATH, jinja2_template as template

@route('/find_snippets')
def snippetHandler():
    query = request.query['query']
    queryLower = query.lower()

    teiUrl = request.query["fsmTeiUrl"]
    r = urllib2.urlopen(teiUrl).read()
    xml = et.fromstring(r)
    text = xml.findall("text")[0] # ignore the header

    targets = []

    def acquireTargets(e):
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
        subbedTarget = re.sub(query, "<mark>" + query + "</mark>", target, flags=re.IGNORECASE)
        myResponse = {'snippet':subbedTarget, 'matches':len(targets), 'fsmTeiUrl':teiUrl}
        return json.dumps(myResponse)
    else:
        # there were no pure matches.  Just get something so the user has a snippet
        something = []
        def acquireSomething(e):
            if len(something): # we got something, halt the recursion
                return
            if e.text and len(e.text.strip()) > 20: # make sure we don't get something short
                something.append(e.text)
            for n in e:
                acquireSomething(n)
        acquireSomething(text)
        myResponse = {'snippet':something[0], 'matches':0, 'fsmTeiUrl':teiUrl}
        return json.dumps(myResponse)

"""
class SnippetHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("query")
        queryLower = query.lower()

        teiUrl = self.request.get("fsmTeiUrl")
        r = urllib2.urlopen(teiUrl).read()
        xml = et.fromstring(r)
        text = xml.findall("text")[0] # ignore the header

        targets = []

        def acquireTargets(e):
            if e.text and e.text.lower().find(queryLower) != -1:
                targets.append(e.text)
            for n in e:
                acquireTargets(n)
            if e.tail and e.tail.lower().find(queryLower) != -1:
                targets.append(e.tail)

        acquireTargets(text)

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')

        if len(targets) != 0:
            # use the first match and highlight it
            target = targets[0]
            subbedTarget = re.sub(query, "<mark>" + query + "</mark>", target, flags=re.IGNORECASE)
            myResponse = {'snippet':subbedTarget, 'matches':len(targets), 'fsmTeiUrl':teiUrl}
            self.response.out.write(json.dumps(myResponse))
        else:
            # there were no pure matches.  Just get something so the user has a snippet
            something = []
            def acquireSomething(e):
                if len(something): # we got something, halt the recursion
                    return
                if e.text and len(e.text.strip()) > 20: # make sure we don't get something short
                    something.append(e.text)
                for n in e:
                    acquireSomething(n)
            acquireSomething(text)
            myResponse = {'snippet':something[0], 'matches':0, 'fsmTeiUrl':teiUrl}
            self.response.out.write(json.dumps(myResponse))
"""