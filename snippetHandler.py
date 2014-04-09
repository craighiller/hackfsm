import webapp2
from google.appengine.api import urlfetch
from xml.etree import ElementTree as et
import json
import re

class SnippetHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("query")
        teiUrl = self.request.get("fsmTeiUrl")
        r = urlfetch.fetch(teiUrl).content
        xml = et.fromstring(r)

        targets = []

        queryLower = query.lower()

        text = xml.findall("text")[0]

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
            target = targets[0]
            subbedTarget = re.sub(query, "<mark>" + query + "</mark>", target,flags=re.IGNORECASE)
            myResponse = {'snippet':subbedTarget, 'matches':len(targets), 'fsmTeiUrl':teiUrl}
            self.response.out.write(json.dumps(myResponse))
        else:
            something = []
            def acquireSomething(e):
                if len(something):
                    return
                if e.text and len(e.text.strip()) > 20:
                    something.append(e.text)
                for n in e:
                    acquireSomething(n)
            acquireSomething(text)
            self.response.out.write(json.dumps({'snippet': something[0], 'matches':0, 'fsmTeiUrl':teiUrl}))