import redis
import paho.mqtt.publish as publish
import json
import myconfig
import logging
import logging.config

# Controls for pool and spa
#
# --[[myconfig.MQTT_PATH]] home
#     --poolSpa
#       -- tempSensor
#          -- poolTemp [99]
#          -- spaTemp [99]
#       -- switchSet
#          -- setSpaBubbles [on||off]
#          -- setSpaWhirlPool [on||off]
#          -- setSpaLights [on||off]
#       -- switchAck
#          -- ackSpaBubbles [on||off]
#          -- ackSpaWhirlPool [on||off]
#          -- ackSpaLights [on||off]
#

r = redis.StrictRedis(host='localhost', port=6379, db=0)
# set up loging
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("poolSpaThing")



class poolSpaThing(object):
    """ control over spa and pool """

    def __init__ (self):
        pass

    def setSpaTemp(self,value):
        """ mqtt staus publish for spa temperature """
        publish.single( myconfig.MQTT_PATH + "/poolSpa/tempSensor/spaTemp", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def getSpaTemp(self):
        """ STRING get spa temperature from redis """
        return r.get("spaTemp")

    def getSpaTempInt(self):
        """ ROUNDED INT get spa temperature from redis """
        return int(round(float(r.get("spaTemp"))))


    def setPoolTemp(self,value):
        """ mqtt staus publish for pool temperature """
        publish.single(myconfig.MQTT_PATH + "/poolSpa/tempSensor/poolTemp", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def getPoolTemp(self):
        """ STRING get pool temperature from redis """
        return r.get("poolTemp")

    def getPoolTempInt(self):
        """ ROUNDED INT get pool temperature from redis """
        return int(round(float(r.get("poolTemp"))))

    def toggleSpaBubbles(self,callingIP):
        """ mqtt call to request spa lights are turned on or off """
        if callingIP.find(myconfig.VALID_IP_MASK , 0 ) < 0:
           logger.info ("IP["+callingIP+"] Not Authorised")
           return

        if r.get("ackSpaBubbles") == "on":
           value = "off"
        else:
           value = "on"
        publish.single(myconfig.MQTT_PATH + "/poolSpa/switchSet/setSpaBubbles", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setSpaBubbles(self,value):
        """ mqtt call to request spa bubbles are turned on or off """
        publish.single(myconfig.MQTT_PATH + "/poolSpa/switchSet/setSpaBubbles", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def toggleSpaPump(self,callingIP):
        """ mqtt call to request spa pump are turned on or off """
        if callingIP.find(myconfig.VALID_IP_MASK , 0 ) < 0:
           logger.info ("IP["+callingIP+"] Not Authorised")
           return

        if r.get("ackSpaPump") == "on":
           value = "off"
        else:
           value = "on"
        publish.single(myconfig.MQTT_PATH + "/poolSpa/switchSet/setSpaPump", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setSpaPump(self,value):
        """ mqtt call to request spa lights are turned on or off """
        publish.single(myconfig.MQTT_PATH + "/poolSpa/switchSet/setSpaPump", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def toggleSpaLights(self,callingIP):
        """ mqtt call to request spa lights are turned on or off """
        if callingIP.find(myconfig.VALID_IP_MASK , 0 ) < 0:
           logger.info ("IP["+callingIP+"] Not Authorised")
           return

        if r.get("ackSpaLights") == "on":
           value = "off"
        else:
           value = "on"
        publish.single(myconfig.MQTT_PATH + "/poolSpa/switchSet/setSpaLights", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setSpaLights(self,value):
        """ mqtt call to request spa lights are turned on or off """
        publish.single(myconfig.MQTT_PATH + "/poolSpa/switchSet/setSpaLights", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setThermostatSpaTemp(self,value):
        """ mqtt publish changein thermostat temperature Values """
        publish.single( myconfig.MQTT_PATH + "/poolSpa/controllerReq/setSpaTemp/", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )


    def thingStatus(self):
        """ return a json object of the current poolSpaThing status """
        return json.dumps ( { "spaTemp":int(round(float(r.get("spaTemp")))),
                              "poolTemp":int(round(float(r.get("poolTemp")))),
                              "spaBubbles":r.get("ackSpaBubbles"),
                              "spaPump":r.get("ackSpaPump"),
                              "spaLights":r.get("ackSpaLights"),
                              "thermostatSpaTemp":r.get("thermostatSpaTemp")
                             }
                          )
