#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import logging
from google.appengine.api import urlfetch
import urllib
import urlparse
from xml.etree import ElementTree as et

from environment_variables import *
 
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def query(q, fl="id"):
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':q,
                          #'fl':fl,
                          'wt':'python',
                          'app_id':FSM_APP_ID,
                          'app_key':FSM_APP_KEY})
    result = urlfetch.fetch(url)
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


def appendToQuery(q, elem):
    if q == '':
        return elem
    return q + ' AND ' + elem

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template("home.html")
        self.response.out.write(template.render(template_values))
        
class SearchHandler(webapp2.RequestHandler):
    def post(self):
        q = self.request.get("search")
        if not self.request.get("text"):
            q = appendToQuery(q, '-fsmTeiUrl:[* TO *]')
        if not self.request.get("image"):
            q = appendToQuery(q, '-fsmImageUrl:[* TO *]')
        #if not self.request.get("video"):
        #    q = appendToQuery(q, '-fsmImageUrl:[* TO *]')
        self.response.out.write(query(q))

class ArticleHandler(webapp2.RequestHandler):
    def get(self):
        myId = self.request.get("id")
        myId = escapeAndFixId(myId)
        info = eval(find(myId))
        info = info["response"]["docs"][0] # get the first doc (should only be one)
        del info['id'] # don't display id
        template_values = {}
        if "fsmImageUrl" in info:
            image_link = info["fsmImageUrl"][-1]
            del info['fsmImageUrl']
            template_values['picture_link'] = image_link
        else:
            teiUrl = info["fsmTeiUrl"][-1]
            r = urlfetch.fetch(teiUrl).content
            xml = et.fromstring(r)
            text = xml.getElementsByTagName("text")[0]
            def dump(e):
                ret_val =  '<%s>' % e.tag
                if e.text:
                    ret_val += e.text
                for n in e:
                    ret_val += dump(n)
                ret_val += '</%s>' % e.tag
                if e.tail:
                    ret_val += e.tail
                return ret_val

            template_values['content'] = dump(text)

        template_values['results'] = info
        template = jinja_environment.get_template("article.html")
        self.response.out.write(template.render(template_values))
      
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/article', ArticleHandler)
], debug=True)

