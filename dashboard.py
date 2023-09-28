from flask import Flask, render_template, url_for, request, redirect, jsonify

import threading
#from main import *
import main
import time
app = Flask(__name__)

statuses = ["IGNORE","UP","UP"]
bsbitrate = ["IGNORE","0","0"]
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
    print(id)
    env_man = main.EnvironmentManager().instance()
    status = main.stop_tower(id,env_man.env1)
    statuses[id] = status

    #render_template('index.html',bspower=statuses, bsbitrate=bsbitrate)
    return redirect('/controllers')
    #except:
        #return 'Error turning off power'
@app.route("/get_bitrate", methods=['GET'])
def get_bitrate():
    for id,status in enumerate(statuses):
        if status == "UP":
            returned_bitrate = main.get_bitrate(id)
            bsbitrate[id] = str(returned_bitrate[0]) + "/" + str(returned_bitrate[1])
        else:
             bsbitrate[id] = "0"
    
    return jsonify(bitrate1=bsbitrate[1],bitrate2=bsbitrate[2])
@app.route("/BS")
def print_status(info):
    info = str(info)
    print_info = "<p>" + info + "</p>\n"
    return print_info

if __name__ == "__main__":
    app.run(debug=True)