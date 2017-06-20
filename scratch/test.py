import json
import redis
import time


poolStats= {'MaxTempEver': 0   , 'MinTempEver': 999, 'Month':[]}

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def getPoolStatistics():

    currentMonthTempSum  = 0
    currentMonthTSSum  = 0
    currentMonth = 0
    currentMonthInc = 0
    currentMonthReadingCount = 0
    maxTempForMonth   = 0
    minTempForMonth   = 999


    poolTempValues = r.lrange("poolTemp:history",0,-1)

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
        if  float(temperature) > float( poolStats ['MaxTempEver'] ) :
            poolStats ['MaxTempEver'] = temperature
            poolStats ['MaxTempEverDate'] = poolTempValues [iCount][tokenInd+1:]

        if  float(temperature) < float( poolStats ['MinTempEver'] ) :
            poolStats ['MinTempEver'] = temperature
            poolStats ['MinTempEverDate'] = poolTempValues [iCount][tokenInd+1:]

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
                poolStats['Month'].append({'MonthInc':currentMonthInc, 'MonthTempAve' : aveMonthTemp,'MonthTSAve' : aveMonthTS,'MaxTempForMonth' : maxTempForMonth,'MinTempForMonth' : minTempForMonth })
            #

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
    poolStats['Month'].append({'MonthInc':currentMonthInc, 'MonthTempAve' : aveMonthTemp,'MonthTSAve' : aveMonthTS,'MaxTempForMonth' : maxTempForMonth,'MinTempForMonth' : minTempForMonth })
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
    print json_string
    #print poolStats

    return



getPoolStatistics()

#for iCount in range( 0,len(poolStats['Month'])):
    #print poolStats['Month'][iCount]['MonthTempAve']
