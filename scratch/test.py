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

    print len(poolTempValues)
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
            aveMonthTemp = currentMonthTempSum / currentMonthReadingCount
            aveMonthTS   = currentMonthTSSum / currentMonthReadingCount
            poolStats['Month'].append({'MonthInc':currentMonthInc, 'MonthTempAve' : aveMonthTemp,'MonthTSAve' : aveMonthTS,'MaxTempForMonth' : maxTempForMonth,'MinTempForMonth' : minTempForMonth })
            #
            print "month " + str(currentMonth) + " inc=" + str(currentMonthInc) + " temp sum=" + str(currentMonthTempSum)+ " temp count=" + str(currentMonthReadingCount)+ " temp TS sum=" + str(currentMonthTSSum)
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
    print poolStats

    return

'''
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

        if  float(temperature) > float(poolStats ['MaxTempFor'+str(tempDateTime[1])]) :
            poolStats ['MaxTempFor'+str(tempDateTime[1])] = temperature
            poolStats ['MaxTempDateFor'+str(tempDateTime[1])] = poolTempValues [iCount][tokenInd+1:]

        if  float(temperature) < float(poolStats ['MinTempFor'+str(tempDateTime[1])]) :
            poolStats ['MinTempFor'+str(tempDateTime[1])] = temperature
            poolStats ['MinTempDateFor'+str(tempDateTime[1])] = poolTempValues [iCount][tokenInd+1:]

            poolStats ['SumTempFor'+str(tempDateTime[1])] += float(temperature)
            poolStats ['SumFor'+str(tempDateTime[1])] += 1


    poolStats ['AverageTemp'] = sumOfTemps/len(poolTempValues)
    poolStats ['AverageFor6'] = poolStats ['SumTempFor6']/poolStats ['SumFor6']
'''


getPoolStatistics()

#testDict = {'MaxTempEver': 0   , 'MinTempEver': '999',
#            'Month': [{'MonthInc':0, 'MonthAve' : 123},{'MonthInc':1, 'MonthAve' : 223}]  };
#testDict = {}
#print "before"
#print testDict['Month']
##print "after"
#testDict['Month'].append({'MonthInc':1, 'MonthAve' : 223})
#print testDict['Month']


#print testDict['Month1'][1]['MonthAve']
#print testDict
#print len(testDict['Month'])

'''
print "Average Temp = " + str(poolStats ['AverageTemp'] )


print "MaxTempEver = " + str(poolStats ['MaxTempEver'] ) + " on " + time.asctime(time.localtime(float(poolStats ['MaxTempEverDate'])))
print "MinTempEver = " + str(poolStats ['MinTempEver'] ) + " on " + time.asctime(time.localtime(float(poolStats ['MinTempEverDate'])))

for iCount in range( 1,13):
    if int(poolStats ['SumFor'+ str(iCount) ]) > 0:
        print "Average " + str(iCount) + " = " +  str( poolStats ['SumTempFor'+ str(iCount)]  / poolStats ['SumFor'+ str(iCount)] )
        print "Max Temp for " + str(iCount) + " = " +  str( poolStats ['MaxTempFor'+ str(iCount)] ) + " on " + time.asctime(time.localtime(float(poolStats ['MaxTempDateFor'+ str(iCount)])))
        print "Min Temp for " + str(iCount) + " = " +  str( poolStats ['MinTempFor'+ str(iCount)] ) + " on " + time.asctime(time.localtime(float(poolStats ['MinTempDateFor'+ str(iCount)])))
'''

#print poolStats
