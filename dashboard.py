from flask import Flask, render_template, url_for, request, redirect


#from main import *
import main
import time
app = Flask(__name__)

statuses = ["IGNORE","UP","UP"]

#To run flask
#flask --app dashboard run 
@app.route("/", methods=['POST', 'GET'])
def hello_world():
    """
    Placeholder
    """
    if request.method == 'POST':
        return ("Gingong")
    else:
        pass
    return render_template('index.html',bspower=statuses)

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

    render_template('index.html',bspower=statuses)  
    
    return redirect('/')
    #except:
        #return 'Error turning off power'
@app.route("/BS")
def print_status(info):
    info = str(info)
    print_info = "<p>" + info + "</p>\n"
    return print_info

if __name__ == "__main__":
    app.run(debug=True)