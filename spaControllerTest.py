import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import redis
import time
import requests
import myconfig
#import requests

#
# test harness for spa controller
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
def on_connect(spaControllerClient, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    spaControllerClient.subscribe(myconfig.MQTT_PATH + "/poolSpa/switchSet/#",qos=0)
    #spaControllerClient.subscribe("#",qos=0)
    #spaControllerClient.subscribe("m2",qos=0)

# The callback for when the client receives a CONNACK response from the server.
# The callback for when a PUBLISH message is received from the server.
def on_message(spaControllerClient, userdata, msg):


    print ("*-- TEST HARNESS -- message received")
    print ( msg.topic +":"+str(msg.payload) )
    topicList = msg.topic.split("/")

    #
    # store temp sensor results
    #
    if ( topicList[0] == myconfig.MQTT_PATH and
         topicList[1] == "poolSpa" and
         topicList[2] == "switchSet" ):

            if topicList[3] == "setSpaBubbles":
                print ( "setSpaBubbles" )
                publish.single( myconfig.MQTT_PATH + "/poolSpa/switchAck/ackSpaBubbles", str(msg.payload), 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT)
                print ( "setSpaBubbles done" )

            if topicList[3] == "setSpaLights":
                print ( "setSpaLights" )
                publish.single(myconfig.MQTT_PATH + "/poolSpa/switchAck/ackSpaLights", str(msg.payload), 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT)

            if topicList[3] == "setSpaPump":
                print ( "setSpaPump" )
                publish.single(myconfig.MQTT_PATH + "/poolSpa/switchAck/ackSpaPump", str(msg.payload), 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT)

            print ("*-- TEST HARNESS -- message processed")
            return

    #
    # if we are here we can ignore the message
    #
    print ("*-- TEST HARNESS -- message ignored")

#
# program body
#

spaControllerClient = mqtt.Client( client_id='spa1' , clean_session=False)
spaControllerClient.on_connect = on_connect
spaControllerClient.on_message = on_message
#spaControllerClient.username_pw_set('admin','scout123')
#
spaControllerClient.connect("localhost", 1883, 60)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

#
# process messages
#
spaControllerClient.loop_forever()
