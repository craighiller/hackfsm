from google.appengine.api import urlfetch
import urllib
from environment_variables import *
import json

def queryPluck(q):
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

def query(q, start="0"):
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':q,
                          'start':start,
                          'wt':'python',
                          'app_id':FSM_APP_ID,
                          'app_key':FSM_APP_KEY})
    result = urlfetch.fetch(url)
    print(url)
    return eval(result.content)

def find(id):
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':'id:' + id,
        'wt':'json',
        'app_id':FSM_APP_ID,
        'app_key':FSM_APP_KEY})
    result = urlfetch.fetch(url)
    return result.content

def escapeAndFixId(id):
    id = id.replace(':', '\:')
    splitted = id.split(' ')
    if len(splitted) == 1:
        return id
    splitted[-2] = splitted[-2] + ' ' + splitted[-1]
    splitted.pop()
    return ''.join(splitted)

def popup(q, collection):
    BASE_URL = "https://www.popuparchive.com:443/api/search?"
    url = "{base_url}".format(base_url=BASE_URL) + urllib.urlencode({
        'query':q,
        'filters[collection_id]':collection
    })
    result = urlfetch.fetch(url)
    j = json.loads(result.content)
    return (j)
    
def getTranscript(item_id, audio_id):
    BASE_URL = "https://www.popuparchive.com:443/api/items/{item_id}/audio_files/{audio_file_id}/transcript"
    url = BASE_URL.format(item_id = item_id, audio_file_id = audio_id)
    print url
    result = urlfetch.fetch(url)
    j = json.loads(result.content)
    return j
    
def appendToQuery(q, elem):
    if q == '':
        return elem
    return q + ' AND ' + elem

tei_to_html_tags = {
    "item":"li",
    "list":"ol",
    "pb":"br"
}

def xmlToHTML(e):
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
