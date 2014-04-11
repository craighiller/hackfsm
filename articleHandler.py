import urllib2
from bottle import request, route, jinja2_template as template
from xml.etree import ElementTree as et
from helper import *

@route('/article')
def articleHandler():
    myId = request.query["id"].replace(':', '\:') # escape the colon metacharacter
    info = find(myId)["response"]["docs"][0] # get the first doc (should only be one)
    del info['id'] # del keys so we don't display them at the bottom
    template_values = {}
    if "fsmImageUrl" in info:
        image_link = info["fsmImageUrl"][-1]
        del info['fsmImageUrl']
        template_values['picture_link'] = image_link
    else:
        teiUrl = info["fsmTeiUrl"][-1]
        del info['fsmTeiUrl']
        r = urllib2.urlopen(teiUrl).read()
        xml = et.fromstring(r)
        text = xml.findall("text")[0] # ignore the TEI header, only get content
        template_values['content'] = xmlToHTML(text)

    template_values['results'] = info
    return template("article.html", template_values)
    