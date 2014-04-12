#!/usr/bin/env python
import sys, os
import logging

package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

import bottle

from bottle import get, route, run, jinja2_template as template
from bottle import static_file, error


from searchHandler import searchHandler
from audioHandler import audioHandler
from articleHandler import articleHandler
from audioSearchHandler import audioSearchHandler
from snippetHandler import snippetHandler

@error(404)
def custom404(error):
    return template("404.html")

@error(500)
def custom500(error):
    return template("500.html")

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@route('/')
def main():
    return template("home.html")

run(host='0.0.0.0', port=80, server="cherrypy")
