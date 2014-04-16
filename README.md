hackFSM
=============
Running on http://2n.io (to be depreciated)

App Engine version: http://fsm-archive.appspot.com/ (on branch gae)

## About

Free Speech Movement

This project was made at the FSM hackathon (4/1/14 - 4/12/14). The project's main intent is to display the archive data in a more manageable format, and provide a clean UI for learning and researching the free speech movement. The API is provided by the Bancroft Library FSM archive accessible though the HTTPS queries with solr.

## Technologies used

- Bottle as web-framework with jinja2 for templates with markupsafe
- CherryPy for server (all included within /packages)
- TimelineJS for timeline on home page (http://timeline.knightlab.com/)

spreadsheet used for timeline data: https://docs.google.com/spreadsheet/ccc?key=0AgsTsRYqkaypdFRPaDY0ZDFmZEZfN0tkT04yU0oxMVE&usp=sharing#gid=0

Templates can be found in the views folder and static files in static folder.
All controllers end with the name Handler.py

## Deployment

### Local
You can just run `python main.py` to start the server and access the app on localhost:port.
Sudo is required to run on port 80, but the port can be changed by altering main.py

### Server
Assuming a fresh Ubuntu 12 instance, run the following commands (replacing `APP_ID` and `APP_KEY` with their values) :
```
sudo apt-get install python
sudo apt-get install git
git clone https://github.com/craighiller/hackfsm
cd hackfsm
printf 'FSM_APP_ID = "APP_ID"\nFSM_APP_KEY = "APP_KEY"' > environment_variables.py
nohup sudo python main.py >> log 2>&1 &
```
The server can be changed to use something other than CherryPy by following instructions on this page: http://bottlepy.org/docs/dev/deployment.html
