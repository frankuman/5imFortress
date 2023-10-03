from flask import Flask, render_template, url_for, request, redirect, jsonify

from SFclasses import class_environment
from api import dashboard_handler
import threading
#from main import *
import main
import time
app = Flask(__name__)

statuses = ["IGNORE","UP","UP"]
bsbitrate = ["IGNORE","0","0"]
bsusers = ["IGNORE", "0", "0"]
#To run flask
#flask --app dashboard run 

@app.route("/", methods=['POST', 'GET'])
def first_request():
    """
    Placeholder
    """
    if request.method == 'POST':
        return ("Gingong")
    else:
        pass
    return render_template('index.html',bspower=statuses)

@app.route("/controllers", methods=['POST', 'GET'])
def hmi_request():
    """
    Placeholder
    """
    if request.method == 'POST':
        return ("Gingong")
    else:
        pass
    return render_template('controllers.html',bspower=statuses, bsbitrate=bsbitrate)
# @app.context_processor
# @app.context_processor
# def bitrate_updater():

#     bitrate_tower, t_bitrate = main.get_bitrate(1)
#     bsbitrate[1] = str(bitrate_tower)
#     bitrate_tower, t_bitrate = main.get_bitrate(2)
#     bsbitrate[2] = str(bitrate_tower)
#     return bsbitrate

@app.route('/power/<int:id>')
def power_off(id):
    """
    Turn off base station, update status in gui
    """
    #try:
    print("TURNING ON/OFF TOWER:",id)
    env_man = class_environment.EnvironmentManager().instance()
    status = dashboard_handler.stop_tower(id,env_man.env1)
    statuses[id] = status

    #render_template('index.html',bspower=statuses, bsbitrate=bsbitrate)
    return jsonify(bsstatus1=statuses[1],bsstatus2=statuses[2])
    #except:
        #return 'Error turning off power'

@app.route("/get_bitrate", methods=['GET'])
def get_bitrate():
    for id,status in enumerate(statuses):
        if status == "UP":
            returned_bitrate = dashboard_handler.get_bitrate(id)
            bsbitrate[id] = str(returned_bitrate[0]) + "/" + str(returned_bitrate[1])
        else:
             bsbitrate[id] = "0"
    
    return jsonify(bitrate1=bsbitrate[1],bitrate2=bsbitrate[2])

@app.route("/get_users", methods=['GET'])
def get_users():
    for id, status in enumerate(statuses):
        if status == "UP":
            returned_users = dashboard_handler.get_users(id)
            bsusers[id] = str(returned_users)
        else:
            bsusers[id] = "0"
        #print(statuses,bsusers)
    return jsonify(bsusers1=bsusers[1],bsusers2=bsusers[2])

@app.route("/get_status", methods=['GET'])
def get_status():
    return jsonify(bsstatus1=statuses[1],bsstatus2=statuses[2])
