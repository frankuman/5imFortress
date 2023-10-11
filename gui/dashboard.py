"""
Flask frontend
Gets information about backend via modbus client/master
"""
import datetime
from flask import Flask, render_template, request, jsonify, redirect, make_response
from flask_login import LoginManager, login_required,login_user
from datalogger import logger
from scada import modbus_master
from SFclasses.user_handler import User, db, LoginForm, generate_random_cookie
import json
import gui_main

app = Flask(__name__)
gui_main.create_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

statuses = ["IGNORE","UP","UP","UP","UP","UP"]
bsbitrate = ["IGNORE","0","0","0","0","0"]
bsusers = ["IGNORE", "0","0","0","0","0"]

current_time = datetime.datetime.now()
time_string = current_time.strftime('%H:%M:%S')
logger.log(0,f"({time_string})-[SERVER] Starting up server on 127.0.0.1:5000")

@app.route("/", methods=["POST", "GET"])
def login():
    """
    For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        print(user)
        if user:
            #if bcrypt.check_password_hash(user.password, form.password.data):
            # // Add encryption here?
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            app.secret_key = generate_random_cookie() #generate new cookie after login
            return redirect("/dashboard")
    return render_template('index.html', form=form)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/dashboard", methods=['POST', 'GET'])
@login_required
def first_request():
    """
    Request site for dashboard
    Returns:
        template: 
    """
    if request.method == 'POST':
        return "5imSERVER ERROR"
    else:
        pass
    return render_template('dashboard.html',bspower=statuses)


@login_manager.unauthorized_handler
def unauthorized():
    """
    Redirect to login page from unauthorized users
    """
    return redirect('/')

@app.route("/controllers", methods=['POST', 'GET'])
@login_required
def hmi_request():
    """
    Request site for HMI
    Returns:
        template: 
    """
    if request.method == 'POST':
        return "5imSERVER ERROR"
    else:
        pass
    return render_template('controllers.html', bspower=statuses, bsbitrate=bsbitrate)

@app.route("/loggers", methods=['POST', 'GET'])
@login_required
def loggers_request():
    """
    Request site for logging
    Returns:
        template: 
    """
    if request.method == 'POST':
        return "5imSERVER ERROR"
    else:
        pass
    return render_template('loggers.html')

@app.route("/loggers/get_log", methods=['POST', 'GET'])
@login_required
def get_log():
    """
    Gets the log for all towers AND the system
    Returns:
        jsonify: all logs
    """
    log1 = logger.read_log(1)
    log2 = logger.read_log(2)
    log3 = logger.read_log(3)
    log4 = logger.read_log(4)
    log5 = logger.read_log(5)
    system_log = logger.read_log(0)

    return jsonify(bslog1=log1, bslog2=log2, bslog3=log3, bslog4=log4, bslog5=log5, systemlog=system_log)

@app.route('/power/<int:id>')
@login_required
def power_off(bs_id):
    """
    Turn off/on base station, update status in gui
    """
    #try:
    if statuses[bs_id] == "UP":
        modbus_master.write_coil(bs_id, 0, "POW")
        statuses[bs_id] = "DOWN"
    else:
        modbus_master.write_coil(bs_id, 1, "POW")
        statuses[bs_id] = "UP"

    print("TURNING ON/OFF TOWER:", id)

    # env_man = class_environment.EnvironmentManager().instance()
    # status = dashboard_handler.stop_tower(id,env_man.env1)
    # statuses[id] = status

    # #render_template('index.html',bspower=statuses, bsbitrate=bsbitrate)
    return jsonify(bsstatus1=statuses[1], bsstatus2=statuses[2], bsstatus3=statuses[3], bsstatus4=statuses[4], bsstatus5=statuses[5])
    #except:
        #return 'Error turning off power'

@app.route("/get_bitrate", methods=['GET'])
@login_required
def get_bitrate():
    """
    Gets the bitrate for all towers
    Returns:
        jsonify: all bitrates
    """

    for bs_id, status in enumerate(statuses):
        if status == "UP":
            returned_bitrate = modbus_master.get_bitrate(bs_id)
            if returned_bitrate is None:

                cur_time = datetime.datetime.now()
                t_string = cur_time.strftime('%H:%M:%S')
                logger.log(0, f"///----({t_string})-MODBUS_MASTER ERROR WITH INFO: - Gettig bitrate did not work as intended///----")

                return jsonify(bitrate1=bsbitrate[1], bitrate2=bsbitrate[2], bitrate3=bsbitrate[3], bitrate4=bsbitrate[4], bitrate5=bsbitrate[5])
            bsbitrate[bs_id] = str(returned_bitrate[0]) + "/" + str(returned_bitrate[1])
        else:
            bsbitrate[bs_id] = "0"
    return jsonify(bitrate1=bsbitrate[1],bitrate2=bsbitrate[2],bitrate3=bsbitrate[3],bitrate4=bsbitrate[4],bitrate5=bsbitrate[5])

@app.route("/get_users", methods=['GET'])
@login_required
def get_users():
    """
    Gets the users to it can display it in the GUI
    Returns:
        jsonify: all the users
    """
    for bs_id, status in enumerate(statuses):
        if status == "UP":
            returned_users = modbus_master.get_users(bs_id)
            bsusers[bs_id] = str(returned_users)
        else:
            bsusers[bs_id] = "0"
        #print(statuses,bsusers)
    return jsonify(bsusers1=bsusers[1], bsusers2=bsusers[2], bsusers3=bsusers[3], bsusers4=bsusers[4], bsusers5=bsusers[5])

@app.route("/get_status", methods=['GET'])
@login_required
def get_status():
    """
    Gets all of the statuses
    Returns:
        jsonify: all statuses from statuseslist
    """
    return jsonify(bsstatus1=statuses[1], bsstatus2=statuses[2], bsstatus3=statuses[3], bsstatus4=statuses[4], bsstatus5=statuses[5])
