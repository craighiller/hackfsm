hackFSM
=============

## About

Free Speech Movement

This project was made at the FSM hackathon (4/1/14 - 4/12/14). The project's main intent is to display the archive data in a more manageable format, and provide a clean UI for learning and researching the free speech movement. The API is provided by the Bancroft Library FSM archive accessible though the HTTPS queries with solr.

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

### Server
Assuming a fresh Ubuntu 12 instance, run the following commands:
```
sudo apt-get install python
sudo apt-get install git
git clone https://github.com/craighiller/hackfsm
cd hackfsm
echo 'FSM_APP_ID = "APP_ID"
FSM_APP_KEY = "APP_KEY"' > environment_variables.py
nohup sudo python main.py >> log 2>&1 &
```
