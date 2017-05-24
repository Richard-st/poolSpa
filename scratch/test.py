import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
print ("hello")
#print (r.llen("poolTemp:history"))
#print (r.lrange("poolTemp:history",0,-1))


poolTempValues = r.lrange("poolTemp:history",0,-1)



print poolTempValues [0]
print poolTempValues [1]
print poolTempValues [2]

tokenInd1=poolTempValues[0].find(":")
print "temp"
print poolTempValues [0][:tokenInd1]
print "timestamp"
print poolTempValues [0][tokenInd1+1:]

#poolTemps = ( {"temp": poolTempValues [0][:tokenInd1] ,"timestamp" :poolTempValues [0][tokenInd1+1:]  } )
#poolTemps.append ( {"temp": poolTempValues [0][:tokenInd1] ,"timestamp" :poolTempValues [0][tokenInd1+1:]  } )

#poolJson =  {u"name":"poolStats"}
#poolJson.update ( {u"temps" : [ poolTemps  ] }  )
#poolJson.update (poolTemps)
#poolTemps = ( {"temp": poolTempValues [0][:tokenInd1] ,"timestamp" :poolTempValues [0][tokenInd1+1:]  } )

print ("============")

# start of json struct
json_string = """
{
    "name": "poolStats",
    "temps":[
"""

# temps of json struct

#int iTempLength = len(poolTempValues);
print len(poolTempValues)

print poolTempValues[len(poolTempValues) -1 ]


if len(poolTempValues) > 0:
    json_string += ( """ {"temp" : """+poolTempValues [0][:tokenInd1]+ """ , "timestamp" : """ + poolTempValues [0][tokenInd1+1:]+"}"   )


for iCount in range( 1,len(poolTempValues)  ):
#for iCount in range( 1,2 ):
    tokenInd=poolTempValues[iCount].find(":")
    json_string += ","
    json_string += ( """ {"temp" : """+poolTempValues [iCount][:tokenInd]+ """ , "timestamp" : """ + poolTempValues [iCount][tokenInd+1:]+"}"   )

# end of json struct

json_string += """
     ]
}"""

print json_string

data = json.loads(json_string)

print json.dumps(data,indent=4)

#print data["temps"][2]






#json.dumps ( {poolTempValues [0] })
