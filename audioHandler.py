from bottle import request, route, jinja2_template as template
from xml.etree import ElementTree as et
from helper import *

@route('/audioId')
def audioHandler():
    """
    Handle gathering information about a single audio article
    Uses the result template
    """
    myId = request.query["id"]
    info = popupFindById(myId)['results'][0] # should only be one
    template_values = {}
    template_values["audioResult"] = info
    template_values["typeOfResource"] = "audio"

    # fake the results field.  This is so it will be easier to do the bib info on the result template
    template_values["results"] = {
        'fsmDateCreated':[info['date_created']], 
        'fsmTitle':[info['title']]
    }
    if 'creator' in info:
        template_values['creator'] = info['creator']

    # clean the transcript of blank transcriptions (to avoid clutter)
    for audioDict in info['audio_files']:
        transcriptArray = getTranscript(info['id'], audioDict['id'])['parts']
        transcript = []
        for elem in transcriptArray:
            if len(elem['text']) != 0:
                transcript.append({'start':elem['start'], 'text':elem['text']})
        audioDict['transcript'] = transcript

    # only show certain things.  Because the user shouldn't care about id, collection title etc.
    template_values["keysToDisplay"] = ['image_files', 'description', 'title', 'date_broadcast', 'date_created', 'series_title']
    return template("result.html", template_values)