import jinja2
import os
import logging

from xml.etree import ElementTree as et

from helper import *

from bottle import request, route, TEMPLATE_PATH, jinja2_template as template

@route('/audioSearch')
def audioSearchHandler():
    """
    Handle searching the popup archive
    Uses the search template
    """
    q = request.query["q"]
    if not q:
        q = "[* TO *]" # blank query, collect all
    collection = request.query.collection
    if not collection:
        collection = 1712 # default to UCSF Archives and Special Collections
    else:
        collection = int(collection)
    results = popup(q, collection)

    # if popup archive returns no results we need to protect ourselves
    if 'results' in results.keys():
        info = results['results']
    else:
        info = ""

    template_values = {}
    template_values["response"] = info
    template_values["collection"] = collection
    template_values["typeOfResource"] = "audio"
    template_values["numPages"] = 1
    template_values["query"] = request.query["q"]
    return template("search.html", template_values)
