from unittest import result
from WebSystem import app
from flask import jsonify, request, render_template
from WebSystem.models import DataManager
from pythonping import ping

route_db = app.config['ROUTE_BBDD']
data_manager = DataManager(route_db)

def login(user, password):
    data = data_manager.user_information_admin()
    for users in data:
        if users["User"] == user:
            user_check = users
    if user_check["User"] == user and str(user_check["Password"]) == password:
        return "Log in"

@app.route("/api/v01/system/<user>/<password>", methods=['GET', 'POST', 'UPDATE'])
def pings(user, password):
    if request.method == 'GET':
        Login = False
        log = login(user, password)
        if log == "Log in":
            Login = True
        else:
            Login = False

        if Login == True:
            machines = data_manager.machines()
            view_machines = jsonify(machines)
            return render_template('index.html', machines=machines)
            #return view_machines
        else:
            return "Usuario y/o contraseña invalido"

    elif request.method == 'POST':
        Login = False
        log = login(user, password)
        if log == "Log in":
            Login = True
        else:
            Login = False

        if Login == True:
            machines = []
            data = data_manager.machines() 
            for ips in data:
                item = ips["IP"]
                machines.append(item)

            list_pings = []
            for machine in machines:
                pings = ping(machine, verbose=True)
                list_pings.append(pings.rtt_avg_ms)

            print(list_pings)

            for ip in data:
                for items in list_pings:
                    print(items)
                    ip["Ping"] = items

            print(data)

            """ results = []
            for row in data:
                respond = {}
                for key, value in zip(row, respond_ping):
                    key["Ping"] = value
                results.append(respond) """

            return data
        else:
            return "Usuario y/o contraseña invalido"            