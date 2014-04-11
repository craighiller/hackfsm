import webapp2
import jinja2
import os
import logging

from xml.etree import ElementTree as et

from helper import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AudioHandler(webapp2.RequestHandler):
    def get(self):
        myId = self.request.get("id")
        info = popupFindById(myId)['results'][0] # should only be one
        template_values = {}
        template_values["audioResult"] = info
        template_values["typeOfResource"] = "audio"
        template_values["results"] = {
            'fsmDateCreated':[info['date_created']], 
            'fsmTitle':[info['title']]
        }
        if 'creator' in info:
            template_values['creator'] = info['creator']

        for audioDict in info['audio_files']:
        	transcriptArray = getTranscript(info['id'], audioDict['id'])['parts']
        	transcript = []
        	for elem in transcriptArray:
        		if len(elem['text']) != 0:
        			transcript.append({'start':elem['start'], 'text':elem['text']})
        	audioDict['transcript'] = transcript
        template_values["keysToDisplay"] = ['image_files', 'description', 'title', 'date_broadcast', 'date_created', 'series_title']
        template = jinja_environment.get_template("article.html")
        self.response.out.write(template.render(template_values))
