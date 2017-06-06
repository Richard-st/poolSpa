import json
import redis
import time

poolStats= {'MaxTempEver': 0   , 'MinTempEver': '999',
            'SumTempFor1': 0.0 , 'SumFor1' : 0 ,
            'SumTempFor2': 0.0 , 'SumFor2' : 0 ,
            'SumTempFor3': 0.0 , 'SumFor3' : 0 ,
            'SumTempFor4': 0.0 , 'SumFor4' : 0 ,
            'SumTempFor5': 0.0 , 'SumFor5' : 0 ,
            'SumTempFor6': 0.0 , 'SumFor6' : 0 ,
            'SumTempFor7': 0.0 , 'SumFor7' : 0 ,
            'SumTempFor8': 0.0 , 'SumFor8' : 0 ,
            'SumTempFor9': 0.0 , 'SumFor9' : 0 ,
            'SumTempFor10': 0.0 , 'SumFor10' : 0 ,
            'SumTempFor11': 0.0 , 'SumFor11' : 0 ,
            'SumTempFor12': 0.0 , 'SumFor12' : 0 }
sumOfTemps  = 0

r = redis.StrictRedis(host='localhost', port=6379, db=0)

poolTempValues = r.lrange("poolTemp:history",0,-1)


for iCount in range( 0,len(poolTempValues)  ):
    tokenInd=poolTempValues[iCount].find(":")

    tempDateTime = time.localtime(float(poolTempValues [iCount][tokenInd+1:]))
    temperature = poolTempValues [iCount][:tokenInd]

    sumOfTemps += float(poolTempValues [iCount][:tokenInd])

    if  float(temperature) > float( poolStats ['MaxTempEver'] ) :
        poolStats ['MaxTempEver'] = temperature
        poolStats ['MaxTempEverDate'] = poolTempValues [iCount][tokenInd+1:]

    if  float(temperature) < float(poolStats ['MinTempEver']) :
        poolStats ['MinTempEver'] = temperature
        poolStats ['MinTempEverDate'] = poolTempValues [iCount][tokenInd+1:]

    poolStats ['SumTempFor'+str(tempDateTime[1])] += float(temperature)
    poolStats ['SumFor'+str(tempDateTime[1])] += 1


poolStats ['AverageTemp'] = sumOfTemps/len(poolTempValues)
poolStats ['AverageFor6'] = poolStats ['SumTempFor6']/poolStats ['SumFor6']

print "Average Temp = " + str(poolStats ['AverageTemp'] )
print "MaxTempEver = " + str(poolStats ['MaxTempEver'] ) + " on " + time.asctime(time.localtime(float(poolStats ['MaxTempEverDate'])))
print "MinTempEver = " + str(poolStats ['MinTempEver'] ) + " on " + time.asctime(time.localtime(float(poolStats ['MinTempEverDate'])))

for iCount in range( 1,13):
    if int(poolStats ['SumFor'+ str(iCount) ]) > 0:
        print "Average " + str(iCount) + " = " +  str( poolStats ['SumTempFor'+ str(iCount)]  / poolStats ['SumFor'+ str(iCount)] )


#print poolStats
