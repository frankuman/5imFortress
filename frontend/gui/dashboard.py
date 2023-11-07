"""
Flask frontend
Gets information about backend via modbus client/master
"""
import datetime
#import json
from flask import Flask, render_template, request, jsonify, redirect
from flask_login import LoginManager, login_required,login_user,utils
from frontend.datalogger import logger
from scada import modbus_master
from frontend.helpers.user_handler import User, db, LoginForm, generate_random_cookie
import gui_main as gui_main

app = Flask(__name__)
gui_main.create_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


statuses = ["IGNORE","UP","UP","UP","UP","UP"]
bsbitrate = ["IGNORE","0","0","0","0","0"]
bsusers = ["IGNORE", "0","0","0","0","0"]
antenna_powers = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]

lastbitrates = [[0, 0], [0, 250000], [0, 100000], [0, 100000], [0, 100000], [0, 100000]]

current_time = datetime.datetime.now()
time_string = current_time.strftime('%H:%M:%S')
logger.log(0,f"({time_string})-[SERVER] Starting up server on 127.0.0.1:5000")

@app.route("/", methods=["POST", "GET"])
def login():
    """
    For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.
    """
    message = ""
    form = LoginForm()
    current_time = datetime.datetime.now()
    time_string = current_time.strftime('%H:%M:%S')
    
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        print(user)

        if user:
            if user.password == form.password.data:
                logger.log(0,f"({time_string})-[SERVER] User {user} successfully logged in")
                # // Add encryption here?
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                if user.accesslevel == "1":
                    app.secret_key = generate_random_cookie() + "x1x0".encode(encoding='utf-8')
                else:
                    app.secret_key = generate_random_cookie() #generate new cookie after login
                
                return redirect("/dashboard")
        logger.log(0,f"({time_string})-[SERVER] User {user} tried to log in")
        message = "Invalid username or password"
    return render_template('index.html', form=form, message=message)

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
    form = LoginForm()
    message = ""
    current_time = datetime.datetime.now()
    time_string = current_time.strftime('%H:%M:%S')
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        

        if user:
            print(user.accesslevel)
            if user.password == form.password.data and user.accesslevel == "1":
                logger.log(0,f"({time_string})-[SERVER]<!IMPORTAN!> User {user} successfully logged into HMI")
                # // Add encryption here?
                user.authenticated = True
                db.session.add(user)
                app.secret_key = generate_random_cookie() + "x1x0".encode(encoding='utf-8')
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/hmi')
            else:
                message = "Invalid credentials or insufficient access level"  # Set the error message for invalid credentials or access level
                logger.log(0,f"({time_string})-[SERVER] User {user} tried to log in to HMI")
                return render_template('controllers.html',form=form, message=message)

        else:
            message = "User not found"  # Set the error message for user not found
            logger.log(0,f"({time_string})-[SERVER] User {user} tried to log in to HMI")
            return render_template('controllers.html',form=form, message=message)


    if(app.secret_key[len(app.secret_key)-4:len(app.secret_key)] == "x1x0".encode(encoding='utf-8')):
        return redirect('/hmi')
    else:
        login_manager.unauthorized()
        print(message)
        return render_template('controllers.html',form=form, message=message)

@app.route("/hmi", methods=['POST', 'GET'])
@login_required
def hmi():
    if(app.secret_key[len(app.secret_key)-4:len(app.secret_key)] != "x1x0".encode(encoding='utf-8')):
            return redirect('/controllers')
    if request.method == 'POST':
        return "5imSERVER ERROR"
    else:
        pass
    return render_template('hmi.html', bspower=statuses, bsbitrate=bsbitrate)


@app.route("/change_gain/<int:gain1>/<int:gain2>/<int:gain3>/<int:gain4>/<int:gain5>", methods=['POST', 'GET'])
@login_required
def send_gain(gain1,gain2,gain3,gain4,gain5):
    """
    Sends gain to master
    """
    gain_list = [gain1,gain2,gain3,gain4,gain5]
    for i in range(5):
        modbus_master.change_gain(i+1,gain_list[i])
    #print("CHANGING GAIN TO",gain_list)
    return jsonify("S")

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

@app.route('/power/<int:bs_id>')
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

    print("TURNING ON/OFF TOWER:", bs_id)

    # env_man = class_environment.EnvironmentManager().instance()
    # status = dashboard_handler.stop_tower(id,env_man.env1)
    # statuses[id] = status

    # #render_template('index.html',bspower=statuses, bsbitrate=bsbitrate)
    return jsonify(bsstatus1=statuses[1], bsstatus2=statuses[2], bsstatus3=statuses[3], bsstatus4=statuses[4], bsstatus5=statuses[5])
    #except:
        #return 'Error turning off power'
@app.route("/antenna_pow/<int:antenna_id>", methods=['POST'])
@login_required
def antenna_power(antenna_id):
    """
    Turn off/on antenna power, update status in gui
    """
    antenna_id = str(antenna_id)
    bs_id = int(antenna_id[0])
    antenna_id = int(antenna_id[1])
    if(antenna_powers[bs_id-1][antenna_id-1] == 1):
        modbus_master.change_antenna_power(bs_id,antenna_id,0)
        antenna_powers[bs_id-1][antenna_id-1] = 0
        print("Turning bs_id",bs_id,"antenna_id",antenna_id,"off")
    elif(antenna_powers[bs_id-1][antenna_id-1] == 0):
        modbus_master.change_antenna_power(bs_id,antenna_id,1)
        antenna_powers[bs_id-1][antenna_id-1] = 1
        print("Turning bs_id",bs_id,"antenna_id",antenna_id,"on")


 

    # #render_template('index.html',bspower=statuses, bsbitrate=bsbitrate)
    return jsonify("Success")
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
    global lastbitrates
    for bs_id, status in enumerate(statuses):
        if status == "UP":
            returned_bitrate = modbus_master.get_bitrate(bs_id)
            if returned_bitrate == False:
                bsbitrate[bs_id] = str(lastbitrates[bs_id][0]) + "/" + str(lastbitrates[bs_id][1])
            else:
                bsbitrate[bs_id] = str(returned_bitrate[0]) + "/" + str(returned_bitrate[1])
                lastbitrates[bs_id][0] = returned_bitrate[0]
                lastbitrates[bs_id][1] = returned_bitrate[1]
            if returned_bitrate is None:
                cur_time = datetime.datetime.now()
                t_string = cur_time.strftime('%H:%M:%S')
                logger.log(0, f"///----({t_string})-MODBUS_MASTER ERROR WITH INFO: - Gettig bitrate did not work as intended///----")

                return jsonify(bitrate1=bsbitrate[1], bitrate2=bsbitrate[2], bitrate3=bsbitrate[3], bitrate4=bsbitrate[4], bitrate5=bsbitrate[5])
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
