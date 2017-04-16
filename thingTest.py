from poolSpaThing import poolSpaThing
import random
import time
import paho.mqtt.publish as publish
import myconfig

rPool = random.randint(1, 50)
rSpa = random.randint(1, 50)
answers = [
    "on",
    "off",
]

# create an instance of my thing

myPoolSpaThing = poolSpaThing()

# request spa bubbles
myPoolSpaThing.setSpaBubbles(random.choice(answers))

# request spa whirlpool
myPoolSpaThing.setSpaPump(random.choice(answers))

# request spa lights
myPoolSpaThing.setSpaLights(random.choice(answers))


# update random spa temp
myPoolSpaThing.setSpaTemp(rSpa)

# update random spa temp

myPoolSpaThing.setPoolTemp(rPool)

#
# Fake answers comming back from spa controller
#

# fake acknowledge spa bubbles
publish.single("/home/poolSpa/switchAck/ackSpaBubbles", random.choice(answers), 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT, auth={'username':'admin','password':'scout123'}  )

# fake acknowledge spa whirlpool
publish.single("/home/poolSpa/switchAck/ackSpaPump", random.choice(answers), 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT, auth={'username':'admin','password':'scout123'}  )

# fake acknowledge spa lights
publish.single("/home/poolSpa/switchAck/ackSpaLights", random.choice(answers), 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT, auth={'username':'admin','password':'scout123'}  )



time.sleep(1)
# request spa lights on
print myPoolSpaThing.thingStatus()
