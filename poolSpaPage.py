from flask import *
from flask_socketio import SocketIO
import requests
import poolSpaThing
import myconfig
import time

app = Flask(__name__)
socketio = SocketIO(app)
myPoolSpaThing = poolSpaThing.poolSpaThing()

@app.route('/old')

def mainPage():
    return render_template('spaController.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )

@app.route('/logger')

def logPage():
    return render_template('spaLogger.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )

@app.route('/admin')

def adminPage():
    return render_template('spaAdmin.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )

@app.route('/pool')

def poolPage():
    return render_template('poolHistory.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )


@app.route('/')

def newPage():
    return render_template('spaController0.html', spaTemp = myPoolSpaThing.getSpaTempInt() , poolTemp = myPoolSpaThing.getPoolTempInt() )



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

@socketio.on('toggleSpaOnOffButton')
def toggleSpaOnOffButton():
        myPoolSpaThing.toggleSpaOnOffButton(request.remote_addr)
        return "1"


@socketio.on('updateSpaThermostatTemp')
def updateSpaThermostatTemp(iSpaThermostatTemp):
        myPoolSpaThing.setThermostatSpaTemp(iSpaThermostatTemp)
        print('received data: ' + str(iSpaThermostatTemp))
        return "1"

@socketio.on('updateThermostatIdleTime')
def updateThermostatIdleTime(iThermostatIdleTime):
        myPoolSpaThing.setThermostatIdleTime(iThermostatIdleTime)
        print('received data: ' + str(iThermostatIdleTime))
        return "1"

@socketio.on('updateThermostatSampleTime')
def updateThermostatSampleTime(iThermostatSampleTime):
        myPoolSpaThing.setThermostatSampleTime(iThermostatSampleTime)
        print('received data: ' + str(iThermostatSampleTime))
        return "1"

@socketio.on('updateThermometerPollTime')
def updateThermometerPollTime(iThermometerPollTime):
        myPoolSpaThing.setThermometerPollTime(iThermometerPollTime)
        print('received data: ' + str(iThermometerPollTime))
        return "1"

@socketio.on('getAllPoolTemps')
def getAllPoolTemps():
        socketio.emit('poolTempList',myPoolSpaThing.getAllPoolTemps() , broadcast=True)
        return "1"

@app.route('/api/pool/',methods=['GET','POST'])
def poolBroadcast():
         socketio.emit('poolTempList',myPoolSpaThing.getAllPoolTemps() , broadcast=True)
         return myPoolSpaThing.getAllPoolTemps()



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=True, port=80)
