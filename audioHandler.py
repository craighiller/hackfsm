import webapp2
import jinja2
import os
import logging

from google.appengine.api import urlfetch
from xml.etree import ElementTree as et

from helper import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AudioHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("q")
        collection = self.request.get("collection")
        x=popup(q, int(collection))['results']
        for i in x:
            #self.response.out.write(i.keys())
            for n in range(len(i['audio_files'])):
                self.response.out.write("<a href='"+i['audio_files'][n]['url']+"'>"+ i['title']+"</a>")
                self.response.out.write("</br>")
            
            self.response.out.write(i['description'])
            
            self.response.out.write("</br></br>")
