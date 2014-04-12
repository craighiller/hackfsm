from xml.etree import ElementTree as et
from helper import *
from bottle import request, route, jinja2_template as template

@route('/audioSearch')
def audioSearchHandler():
    """
    Handle searching the popup archive
    Uses the search template
    """
    q = request.query["search"]
    if not q:
        q = "[* TO *]" # blank query, collect all
    collection = request.query.collection
    if not collection:
        collection = 1712 # default to UCSF Archives and Special Collections
    else:
        collection = int(collection)

    template_values = {}

    start = request.query.start
    if not start:
        # no start parameter
        # we need query parameters so that the page links at the bottom of search will look right
        template_values["queryParameters"] = request.query_string
        start = 1
    else:
        # using a start page parameter.  Parse it off so we can reconstruct paging links properly
        template_values["queryParameters"] = "&".join(request.query_string.split('&')[:-1])

    results = popup(q, collection, start)

    # if popup archive returns no results we need to protect ourselves
    if 'results' in results.keys():
        info = results['results']
    else:
        info = ""

    template_values["response"] = info
    template_values["collection"] = collection
    template_values["typeOfResource"] = "audio"
    template_values["numPages"] = 1 # only use one page to display the audio results (Don't think there are more)
    template_values["query"] = request.query["search"]
    return template("search.html", template_values)
