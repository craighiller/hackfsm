#!/usr/bin/env python

import sys, os

package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

import bottle

from bottle import get, route, run, TEMPLATE_PATH, jinja2_template as template
from bottle import static_file

from searchHandler import searchHandler
from audioHandler import audioHandler
from articleHandler import articleHandler
from audioSearchHandler import audioSearchHandler
from snippetHandler import snippetHandler

TEMPLATE_PATH.append("./templates")

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@route('/')
def main():
    return template("home.html")

run(host='localhost', port=8000, debug=True)

