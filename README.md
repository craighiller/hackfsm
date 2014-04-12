hackFSM
=============

## About

Free Speech Movement

This project was made at the FSM hackathon which occured from 4/1/14 - 4/12/14.
The API is provided by the Bancroft Library FSM archive accessible though
the HTTPS queries with solr.

The project's main intent is to display the archive data in a more manageable format,
and provide a clean UI for learning and researching the free speech movement.

## Technologies used

Python is required

Uses Bottle to serve webpages, jinja2 for templates (with markupsafe),
and CherryPy as a server (all included within /packages)

Templates in the views folder, static files in static folder
All controllers end with the name Handler.py

## Deployment

### Local
You can just run `python main.py` to start the server, app should be accessible on localhost:port.
Sudo is required to run on port 80, but the port can be changed by altering main.py
