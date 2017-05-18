
import paho.mqtt.client as mqtt
import redis
import time
import requests
import myconfig
import logging
import logging.config
import json

#import requests

#
# subscribe to MQTT channel and call api endpoint with details
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


# The callback for when the client receives a CONNACK response from the server.
def on_connect(poolTempClient, userdata, flags, rc):

    logger.info("Connected with result code: "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    poolTempClient.subscribe("#",qos=0)
    #poolTempClient.subscribe("m2",qos=0)

# The callback for when the client receives a CONNACK response from the server.
# The callback for when a PUBLISH message is received from the server.
def on_message(poolTempClient, userdata, msg):

    ts = time.time()


    logger.info("message in: "+msg.topic +":"+str(msg.payload) )
    topicList = msg.topic.split("/")


    #
    # Device logging message
    #
    try:
      if ( topicList[0] == myconfig.MQTT_PATH and
           topicList[1] == "logger" ):
           # post log message SocketIO broadcast of status
           requests.get("http://localhost/api/poolSpaLoggerBroadcast/?logLine=" + str(msg.payload) )
    except:
      logger.info("failed to send Device logging message" )


    #
    # Device status message
    #
    try:
        if ( topicList[0] == myconfig.MQTT_PATH and
            topicList[1] == "poolSpa" and
            topicList[2] == "controllerAck" and
            topicList[3] == "getStatus" ):

         # import message and store in redis

		       jStatus = json.loads( str(msg.payload))
		       r.set("thermostatSpaTemp", jStatus['iSpaTemp'] )
		       r.set("thermostatIdleTime", jStatus['iThermoIdleTime'] )
		       r.set("thermostatSampleTime", jStatus['iThermoSampleTime'] )
		       r.set("thermometerPollTime", jStatus['iThermPollTime'] )
		       r.set("SSID", jStatus['cSSid'] )
		       r.set("MQTTServer", jStatus['cServer'] )
		       requests.get("http://localhost/api/poolSpaStatusBroadcast/")
		       logger.info("message processed " )

		       return
    except:
      logger.info("failed to send Device status message " )




    #
    # store temp sensor results
    #
    try:
      if ( topicList[0] == myconfig.MQTT_PATH and
          topicList[1] == "poolSpa" and
          topicList[2] == "tempSensor" ):
             # set current temp
             r.set(topicList[3], str(msg.payload))

             # add historic temperature
             r.lpush(topicList[3]+":history", str(msg.payload) + ":" + str(int(ts))  )

             # push temperature to thingspeak
             if (topicList[3] == "spaTemp"):
               requests.get("https://api.thingspeak.com/update?key="+myconfig.THINGSPEAK_API_KEY+"&field1="+str(msg.payload))

             if (topicList[3] == "poolTemp"):
               requests.get("https://api.thingspeak.com/update?key="+myconfig.THINGSPEAK_API_KEY+"&field2="+str(msg.payload))

             # post stauts SocketIO broadcast of status
             requests.get("http://localhost/api/poolSpaStatusBroadcast/")
             logger.info("message processed " )

             return
    except:
      logger.info("failed to store temp sensor results " )


    #
    # store switch acknowledge status
    #
    try:
      if ( topicList[0] == myconfig.MQTT_PATH and
           topicList[1] == "poolSpa" and
           topicList[2] == "switchAck" ):
              # store result in redis
              r.set(topicList[3], str(msg.payload))

              # post stauts SocketIO broadcast of status
              requests.get("http://localhost/api/poolSpaStatusBroadcast/")


              logger.info("message processed " )
              return
      #
      # if we are here we can ignore the message
      #
      logger.info("message ignored " )
    except:
      logger.info("failed to tore switch acknowledge status " )

    logger.info("Debug 4 " )

#
# program body
#


# set up loging

logging.config.fileConfig("logger.conf")

# create logger
logger = logging.getLogger("mqttSub")


# -----------------------------------------

poolTempClient = mqtt.Client( client_id='home' , clean_session=False)
poolTempClient.on_connect = on_connect
poolTempClient.on_message = on_message
#poolTempClient.username_pw_set('admin','scout123')poolTempClient.username_pw_set('admin','scout123')
#

#poolTempClient.connect("stanners.co.nz", 1883, 60)
poolTempClient.connect("localhost", 1883, 60)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

#
# process messages
#
poolTempClient.loop_forever()
