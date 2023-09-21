from flask import Flask
#from main import *
import main
import time
app = Flask(__name__)

@app.route("/")
#To run flask
#flask --app dashboard run 
def hello_world():
    return "<p>5imFortress</p>"

@app.route("/BS")
def print_status(info):
    info = str(info)
    print_info = "<p>" + info + "</p>\n"
    return print_info