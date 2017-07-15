import sys
sys.path.insert(0, '/home/pi/poolSpa')
import time
import subprocess, signal
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import myconfig

spaAlive = True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(pongClient, userdata, flags, rc):

    print("Connected with result code: "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    pongClient.subscribe("home/pong",qos=0)
    #poolTempClient.subscribe("m2",qos=0)

# The callback for when the client receives a CONNACK response from the server.
# The callback for when a PUBLISH message is received from the server.
def on_message(pongClient, userdata, msg):
    global spaAlive
    topicList = msg.topic.split("/")
    try:
        if ( topicList[0] == myconfig.MQTT_PATH and
            topicList[1] == "pong" ):
            # send back a pong
            spaAlive = True
    except BaseException as e:
        print("failed while receiving pong:" + str(e) )



def main():
    global spaAlive

    print "Spa Watchdog Starting"
    pongClient = mqtt.Client( client_id='pongClient' , clean_session=False)
    pongClient.on_connect = on_connect
    pongClient.on_message = on_message
    pongClient.connect("localhost", 1883, 60)




    try:
        while True:

            pongClient.loop_start()

            try:
                #
                #send out a ping
                #
                spaAlive = False
                publish.single( myconfig.MQTT_PATH + "/ping", '', 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT)
            except BaseException as e:
                print("failed to send ping:" + str(e) )

            time.sleep(10)
            pongClient.loop_stop()

            print ("spa Alive = " + str(spaAlive) )

            #
            # if we cannot find mqtt Kill and restart
            #
            if spaAlive==False:

                p = subprocess.Popen(['ps', '-A','-o','pid,command'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                for line in out.splitlines():
                    if 'mqttSub' in line:
                        pid = int(line.split(None, 1)[0])
                        print "line = " + line
                        os.kill(pid, signal.SIGKILL)
                    if 'poolSpaPage' in line:
                        pid = int(line.split(None, 1)[0])
                        print "line = " + line
                        os.kill(pid, signal.SIGKILL)

                print "starting poolSpaPage"
                print os.spawnl(os.P_NOWAIT, '/usr/bin/python', 'python' ,'/home/pi/poolSpa/poolSpaPage.py')

                print "starting mqttSub"
                print os.spawnl(os.P_NOWAIT, '/usr/bin/python', 'python' ,'/home/pi/poolSpa/mqttSub.py')

                time.sleep(2)



    except KeyboardInterrupt:
        print "Goodbye"
        sys.exit()



if __name__ == "__main__":
    main()
