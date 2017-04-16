from flask import *
from flask_socketio import SocketIO
import requests
import poolSpaThing
import myconfig
import time

app = Flask(__name__)
socketio = SocketIO(app)
myPoolSpaThing = poolSpaThing.poolSpaThing()

@app.route('/')

def mainPage():
    return render_template('spaController.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )

@app.route('/logger')

def logPage():
    return render_template('spaLogger.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )


@app.route('/api/wunderground/')

def wunderground():
        r = requests.get("http://api.wunderground.com/api/e329ec6759d48252/forecast10day/q/NZ/auckland.json")

        return r.text

@app.route('/api/poolSpaStatusBroadcast/',methods=['GET','POST'])
def poolSpaStatusBroadcast():
         socketio.emit('poolSpaStatusUpdate', myPoolSpaThing.thingStatus() , broadcast=True)
         return myPoolSpaThing.thingStatus()


@app.route('/api/poolSpaLoggerBroadcast/',methods=['GET','POST'])
def poolSpaLoggerBroadcast():
         socketio.emit('poolSpaLoggerUpdate', request.args.get('logLine','') , broadcast=True)
         return "return value "+ request.args.get('logLine','')


@socketio.on('toggleSpaBubbles')
def toggleSpaBubbles():
        myPoolSpaThing.toggleSpaBubbles(request.remote_addr)
        return "1"

@socketio.on('toggleSpaLights')
def toggleSpaLight():
        myPoolSpaThing.toggleSpaLights(request.remote_addr)
        return "1"


@socketio.on('toggleSpaPump')
def toggleSpaPump():
        myPoolSpaThing.toggleSpaPump(request.remote_addr)
        return "1"



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=True, port=80)
