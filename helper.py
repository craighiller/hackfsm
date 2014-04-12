import urllib2
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
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({
        'q':q,
        'wt':'python',
        'app_id':FSM_APP_ID,
        'app_key':FSM_APP_KEY,
        'facet':'true',
        'facet.field':'fsmTypeOfResource',
        'facet.mincount':1
    })
    result = urllib2.urlopen(url)
    return eval(result.read())

def query(q, start="0", rowsPerPage="15"):
    """
    Helper to send and evaluate queries to FSM archive
    Returns a python dictionary
    """
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({
        'q':q,
        'start':start,
        'wt':'python',
        'app_id':FSM_APP_ID,
        'app_key':FSM_APP_KEY,
        'rows':rowsPerPage
    })
    result = urllib2.urlopen(url)
    return eval(result.read())

def find(id):
    """
    Helper to find a single article in the FSM article by id
    Returns a python dictionary
    """
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({
        'q':'id:' + id,
        'wt':'json',
        'app_id':FSM_APP_ID,
        'app_key':FSM_APP_KEY
    })
    result = urllib2.urlopen(url)
    return eval(result.read())

def popup(q, collection, page):
    """
    Helper to send and evaluate queries to the popup archive
    Returns a json dictionary
    """
    BASE_URL = "https://www.popuparchive.com:443/api/search?"
    url = "{base_url}".format(base_url=BASE_URL) + urllib.urlencode({
        'query':q,
        'filters[collection_id]':collection,
        'page':page
    })
    result = urllib2.urlopen(url)
    return json.loads(result.read())

def popupFindById(id):
    """
    Helper to find a single audio article in the popup article by id
    Returns a json dictionary
    """
    BASE_URL = "https://www.popuparchive.com:443/api/search?"
    url = "{base_url}".format(base_url=BASE_URL) + urllib.urlencode({
        'query':'id:' + id,
    })
    result = urllib2.urlopen(url)
    return json.loads(result.read())
    
def getTranscript(item_id, audio_id):
    """
    Helper to collect the transcript for a single item/audio
    pair from the popup archive
    Returns a json dictionary
    """
    BASE_URL = "https://www.popuparchive.com:443/api/items/{item_id}/audio_files/{audio_file_id}/transcript"
    url = BASE_URL.format(item_id = item_id, audio_file_id = audio_id)
    result = urllib2.urlopen(url)
    return json.loads(result.read())
    
def appendToQuery(q, elem):
    """
    Helper to extend a query (for use in the fsm archive).  
    Should have an AND condition between query elements if not the first part of the query
    """
    if q == '':
        return elem
    return q + ' AND ' + elem

tei_to_html_tags = {
    "list":"ol",
    "item":"li",
    "pb":"br"
}

def xmlToHTML(xml):
    """
    Converts a XML tree to an appropriate HTML string 
    by converting tags that don't exist in HTML to their
    matches.
    """
    if xml.tag in ['lb', 'salute', 'signed']:
        tag_to_use = 'br'
    elif xml.tag == 'q':
        if 'blockquote' in xml.attrib.values():
            tag_to_use = 'blockquote'
    elif xml.tag == 'emph':
        if 'italics' in xml.attrib.values():
            tag_to_use = 'em'
        elif 'bold' in xml.attrib.values():
            tag_to_use = 'b'
        elif 'under' in xml.attrib.values():
            tag_to_use = 'u'
    elif xml.tag in tei_to_html_tags:
        tag_to_use = tei_to_html_tags[xml.tag]
    else:
        tag_to_use = xml.tag
    ret_val =  '<%s>' % tag_to_use
    if xml.text:
        ret_val += xml.text
    for child in xml:
        ret_val += xmlToHTML(child)
    if xml.tag == 'signed':
        ret_val += '<br><br>'
    elif not xml.tag in ['lb', 'dateline', 'salute']:
        ret_val += '</%s>' % tag_to_use
    if xml.tail:
        ret_val += xml.tail
    return ret_val
