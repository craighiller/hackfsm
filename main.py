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

from environment_variables import *
 
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def query(q, fl="id"):
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':q,
                          'fl':fl,
                          'wt':'python',
                          'app_id':FSM_APP_ID,
                          'app_key':FSM_APP_KEY})
    result = urlfetch.fetch(url)
    return eval(result.content)

def find(id):
    BASE_URL = 'https://apis.berkeley.edu/solr/fsm/select'
    url = "{base_url}?".format(base_url=BASE_URL) + urllib.urlencode({'q':'id:' + id,
        'wt':'python',
        'app_id':FSM_APP_ID,
        'app_key':FSM_APP_KEY})
    result = urlfetch.fetch(url)
    return result.content


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template("home.html")
        self.response.out.write(template.render(template_values))
        
class SearchHandler(webapp2.RequestHandler):
    def post(self):
        q = self.request.get("search")
        if not self.request.get("text"):
            q = q + ' AND -fsmTeiUrl:[* TO *]'
        self.response.out.write(query(q))
        self.response.out.write("</br></br>"+self.request.get("text")+"</br></br>"+self.request.get("image")+"</br></br>"+self.request.get("video"))

class ArticleHandler(webapp2.RequestHandler):
    def get(self):
        myId = self.request.get("id")
        self.response.out.write(find(myId))
      
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/article', ArticleHandler)
], debug=True)

