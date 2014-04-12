from bottle import redirect, route, request, jinja2_template as template
from helper import appendToQuery, query, queryPluck
from xml.etree import ElementTree as et

import cgi

@route('/search')
def searchHandler():
    """
    Handles all search requests.  If it is directed at the popup archive
    then redirects the request to audioSearchHandler. Otherwise it handles
    the FSM archive setup.
    """
    q = request.query.search
    typeOfResource = request.query.type
    if typeOfResource == "audio":
        # if audio let the audioSearchHandler get this with a redirect
        temp = ''
        if 'collectionFilter' in request.query:
            temp += '&collection=' + request.query.collectionFilter
        if 'start' in request.query:
            temp += '&start=' + request.query.start
        return redirect("/audioSearch?type=audio&search=" + q + temp)
    elif typeOfResource == "image":
        q = appendToQuery(q, '-fsmTeiUrl:[* TO *]') # don't show written text
    else:
        q = appendToQuery(q, '-fsmImageUrl:[* TO *]') # don't show images

    typesOfResourcesList = queryPluck(q)['facet_counts']['facet_fields']['fsmTypeOfResource']
    typesOfResourcesDict = {'other':0}
    # generate a dictionary of the top 5 and collect everything else to other
    for i in xrange(0, len(typesOfResourcesList), 2):
        if i >= 10:
            typesOfResourcesDict['other'] += typesOfResourcesList[i+1]
        else:
            typesOfResourcesDict[typesOfResourcesList[i]] = typesOfResourcesList[i+1]

    filterType = request.query.getall('filterType')
    if 'other' in filterType: 
        # exclude what is not in the filterType
        exclusion = set(typesOfResourcesDict.keys()) - set(filterType) - set('other')
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
    start = request.query.start
    if not start:
        # no start parameter
        # we need query parameters so that the page links at the bottom of search will look right
        template_values["queryParameters"] = request.query_string
        start = 1
    else:
        # using a start page parameter.  Parse it off so we can reconstruct paging links properly
        template_values["queryParameters"] = "&".join(request.query_string.split('&')[:-1])

    rowsPerPage = 15
    startRow = (int(start) - 1)*rowsPerPage
    results = query(q, startRow, rowsPerPage)

    template_values["typeOfResource"] = typeOfResource
    template_values['types'] = typesOfResourcesDict
    template_values['filterType'] = filterType
    template_values["query"] = cgi.escape(request.query.search) # block XSS with cgi escape
    template_values["numPages"] = (results["response"]["numFound"] // rowsPerPage) + 1
    template_values["response"] = results["response"]["docs"]
    return template("search.html", template_values)
