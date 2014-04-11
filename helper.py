from google.appengine.api import urlfetch
import urllib
from environment_variables import *
import json

def queryPluck(q):
    """
    Generate a facet for fsmTypeOfResource. This allows us to get
    a list of type and count in the 'facet_count' field
    Returns a python dictionary
    """
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':q,
                          'wt':'python',
                          'app_id':FSM_APP_ID,
                          'app_key':FSM_APP_KEY,
                          'facet':'true',
                          'facet.field':'fsmTypeOfResource',
                          'facet.mincount':1})
    result = urlfetch.fetch(url)
    return eval(result.content)

def query(q, start="0", rowsPerPage="30"):
    """
    Helper to send and evaluate queries to FSM archive
    Returns a python dictionary
    """
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':q,
                          'start':start,
                          'wt':'python',
                          'app_id':FSM_APP_ID,
                          'app_key':FSM_APP_KEY,
                          'rows':rowsPerPage})
    result = urlfetch.fetch(url)
    return eval(result.content)

def find(id):
    """
    Helper to find a single article in the FSM article by id
    Returns a python dictionary
    """
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':'id:' + id,
        'wt':'json',
        'app_id':FSM_APP_ID,
        'app_key':FSM_APP_KEY})
    result = urlfetch.fetch(url)
    return eval(result.content)

def popup(q, collection):
    BASE_URL = "https://www.popuparchive.com:443/api/search?"
    url = "{base_url}".format(base_url=BASE_URL) + urllib.urlencode({
        'query':q,
        'filters[collection_id]':collection
    })
    result = urlfetch.fetch(url)
    j = json.loads(result.content)
    return j

def popupFindById(id):
    BASE_URL = "https://www.popuparchive.com:443/api/search?"
    url = "{base_url}".format(base_url=BASE_URL) + urllib.urlencode({
        'query':'id:' + q,
    })
    result = urlfetch.fetch(url)
    j = json.loads(result.content)
    return j
    
def getTranscript(item_id, audio_id):
    BASE_URL = "https://www.popuparchive.com:443/api/items/{item_id}/audio_files/{audio_file_id}/transcript"
    url = BASE_URL.format(item_id = item_id, audio_file_id = audio_id)
    result = urlfetch.fetch(url)
    j = json.loads(result.content)
    return j
    
def appendToQuery(q, elem):
    """
    Helper to extend a query.  Should have an AND condition between
    if not the first part of the query
    """
    if q == '':
        return elem
    return q + ' AND ' + elem

tei_to_html_tags = {
    "item":"li",
    "list":"ol",
    "pb":"br"
}

def xmlToHTML(e):
    """
    Converts a XML tree to an approximate HTML tree.
    Works in conjunction with tei_to_html_tags
    to convert tags that don't exist in HTML
    """
    if e.tag in ['lb', 'salute', 'signed']:
        tag_to_use = 'br'
    elif e.tag in tei_to_html_tags:
        tag_to_use = tei_to_html_tags[e.tag]
    else:
        tag_to_use = e.tag
    ret_val =  '<%s>' % tag_to_use
    if e.text:
        ret_val += e.text
    for n in e:
        ret_val += xmlToHTML(n)
    if e.tag == 'signed':
        ret_val += '<br><br>'
    elif not e.tag in ['lb', 'dateline', 'salute']:
        ret_val += '</%s>' % tag_to_use
    if e.tail:
        ret_val += e.tail
    return ret_val
