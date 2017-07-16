import redis
import paho.mqtt.publish as publish
import json
import myconfig
import logging
import logging.config
import time

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
logging.config.fileConfig("/home/pi/poolSpa/logger.conf")
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


    def toggleSpaOnOffButton(self,callingIP):
        """ mqtt call to request spa On or Off """
        if callingIP.find(myconfig.VALID_IP_MASK , 0 ) < 0:
           logger.info ("IP["+callingIP+"] Not Authorised")
           return

        if r.get("OnOff") == "off":
           value = "on"
        else:
           value = "off"
        publish.single(myconfig.MQTT_PATH + "/poolSpa/controllerReq/OnOff/", value, 1, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT ,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )



    def setThermostatSpaTemp(self,value):
        """ mqtt publish changein thermostat temperature Values """
        publish.single( myconfig.MQTT_PATH + "/poolSpa/controllerReq/setSpaTemp/", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setThermostatIdleTime(self,value):
        """ mqtt publish changein thermostat Idle Time """
        publish.single( myconfig.MQTT_PATH + "/poolSpa/controllerReq/setThermoIdleTime/", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setThermostatSampleTime(self,value):
        """ mqtt publish change in thermostat Sample Time """
        publish.single( myconfig.MQTT_PATH + "/poolSpa/controllerReq/setThermoSampleTime/", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )

    def setThermometerPollTime(self,value):
        """ mqtt publish changein thermometer poll time """
        publish.single( myconfig.MQTT_PATH + "/poolSpa/controllerReq/setThermPollTime/", value, 0, False, hostname=myconfig.MQTT_SERVER, port=myconfig.MQTT_PORT,
        auth={'username' : myconfig.MQTT_USER , 'password' : myconfig.MQTT_PASSWORD} )


    def thingStatus(self):
        """ return a json object of the current poolSpaThing status """
        return json.dumps ( { "spaTemp":int(round(float(r.get("spaTemp")))),
                              "spaTempFloat":r.get("spaTemp"),
                              "poolTemp":int(round(float(r.get("poolTemp")))),
                              "spaBubbles":r.get("ackSpaBubbles"),
                              "spaPump":r.get("ackSpaPump"),
                              "spaLights":r.get("ackSpaLights"),
                              "SSID":r.get("SSID"),
                              "MQTTServer":r.get("MQTTServer"),
                              "thermostatSpaTemp":r.get("thermostatSpaTemp"),
                              "thermostatIdleTime":r.get("thermostatIdleTime"),
                              "thermostatSampleTime":r.get("thermostatSampleTime"),
                              "thermometerPollTime":r.get("thermometerPollTime"),
                              "spaPowerButton":r.get("OnOff")
                             }
                          )



    def getAllPoolTemps(self):
        currentMonthTempSum  = 0
        currentMonthTSSum  = 0
        currentMonth = 0
        currentMonthInc = 0
        currentMonthReadingCount = 0
        maxTempForMonth   = 0
        minTempForMonth   = 999

        poolTempValues = r.lrange("poolTemp:history",0,-1)
        poolStats= {'maxTempEver': 0   , 'minTempEver': 999, 'months':[]}


        if len(poolTempValues)== 0:  #bail if no values returned
            return

        # Setup start value
        tokenInd=poolTempValues[0].find(":")
        tempDateTime = time.localtime(float(poolTempValues [0][tokenInd+1:]))
        currentMonth = tempDateTime[1]

        for iCount in range(len(poolTempValues)-1,-1,-1  ):
            #
            # breakdown readings into managable tokens
            #
            tokenInd     = poolTempValues[iCount].find(":")
            tempDateTime = time.localtime(float(poolTempValues [iCount][tokenInd+1:]))
            tempMonth    = tempDateTime[1]
            temperature  = poolTempValues [iCount][:tokenInd]

            #
            # update for max and min forever temps
            #
            if  float(temperature) > float( poolStats ['maxTempEver'] ) :
                poolStats ['maxTempEver'] = temperature
                poolStats ['maxTempEverDate'] = poolTempValues [iCount][tokenInd+1:]

            if  float(temperature) < float( poolStats ['minTempEver'] ) :
                poolStats ['minTempEver'] = temperature
                poolStats ['minTempEverDate'] = poolTempValues [iCount][tokenInd+1:]

            #
            # Have we started a new month
            #
            if tempMonth != currentMonth:
                #
                #update dictionary for ending month
                #
                if currentMonthReadingCount > 0 :
                    aveMonthTemp = currentMonthTempSum / currentMonthReadingCount
                    aveMonthTS   = currentMonthTSSum / currentMonthReadingCount
                    poolStats['months'].append({'monthInc':currentMonthInc, 'monthTempAve' : aveMonthTemp,'monthTSAve' : aveMonthTS,'maxTempForMonth' : maxTempForMonth,'minTempForMonth' : minTempForMonth })
                    #
                    #print "month " + str(currentMonth) + " inc=" + str(currentMonthInc) + " temp sum=" + str(currentMonthTempSum)+ " temp count=" + str(currentMonthReadingCount)+ " temp TS sum=" + str(currentMonthTSSum)
                    #
                    #reset for new month
                    #
                    currentMonth = tempMonth
                    currentMonthInc +=1
                    currentMonthTempSum  = 0
                    currentMonthReadingCount = 0
                    currentMonthTSSum = 0
                    maxTempForMonth   = 0
                    minTempForMonth   = 999

            #
            # Update month values
            #
            currentMonthTempSum += float(poolTempValues [iCount][:tokenInd])
            currentMonthReadingCount +=1
            currentMonthTSSum += float(poolTempValues [iCount][tokenInd+1:])

            #
            # update for max and min for month
            #
            if  float(temperature) > maxTempForMonth :
                maxTempForMonth = float(temperature)

            if  float(temperature) < minTempForMonth :
                minTempForMonth = float(temperature)

        #
        #update dictionary for final month
        #
        aveMonthTemp = currentMonthTempSum / currentMonthReadingCount
        aveMonthTS   = currentMonthTSSum / currentMonthReadingCount
        poolStats['months'].append({'monthInc':currentMonthInc, 'monthTempAve' : aveMonthTemp,'monthTSAve' : aveMonthTS,'maxTempForMonth' : maxTempForMonth,'minTempForMonth' : minTempForMonth })
        #


        #---------------------------------------
        # start of json struct
        #---------------------------------------
        json_string = '{"name":"poolStats","temps":['
        # temps of json struct
        if len(poolTempValues) > 0:
            tokenInd=poolTempValues[len(poolTempValues)-1].find(":")
            json_string += ( """ {"temp" : """+poolTempValues [len(poolTempValues)-1][:tokenInd]+ """ , "timestamp" : """ + poolTempValues [len(poolTempValues)-1][tokenInd+1:]+"}"   )

        for iCount in xrange(  len(poolTempValues)-2, -1, -1  ):
            tokenInd=poolTempValues[iCount].find(":")
            json_string += ","
            json_string += ( """ {"temp" : """+poolTempValues [iCount][:tokenInd]+ """ , "timestamp" : """ + poolTempValues [iCount][tokenInd+1:]+"}"   )

        # end of json struct
        json_string += """
        ]"""

        # add stats (changing first { for ,)
        json_string += json.dumps(poolStats).replace('{', ',', 1)

        return json.dumps ( json.loads(json_string))
