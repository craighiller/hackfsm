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
        if not q:
            q = ""
        collection = self.request.get("collection")
        if not collection:
            collection = 1712
        info = popup(q, int(collection))['results']
        template_values = {}
        template_values["response"] = info
        template_values["typeOfResource"] = "audio"
        template = jinja_environment.get_template("audioSearch.html")
        self.response.out.write(template.render(template_values))

        return

        for i in info:
            #self.response.out.write(i.keys())
            #self.response.out.write("Identifier: "+ str(i['identifier'])+"</br></br>")
            
            for n in range(len(i['audio_files'])):
                self.response.out.write("<a href='"+i['audio_files'][n]['url']+"'>"+ i['title']+"</a>")
                self.response.out.write("</br>"+"ID: "+ str(i['id'])+"</br>")
                self.response.out.write("Audio ID: "+ str(i['audio_files'][n]['id']))
                self.response.out.write("</br>")
                self.response.out.write("Transcript: </br>"+str(getTranscript(i['id'],i['audio_files'][n]['id'] )))
            
            self.response.out.write(i['description'])
            
            self.response.out.write("</br></br>")
