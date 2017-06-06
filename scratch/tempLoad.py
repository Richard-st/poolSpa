import redis
import time
import random


r = redis.StrictRedis(host='localhost', port=6379, db=0)

poolTempValues = r.lrange("poolTemp:history",0,-1)


xtimedate = time.time()


for index in range(1,400):
   print index
   #xtimedate =  timedelta(hours=index)
   randomishTemp =  20.0 + (random.random()*10)
   print randomishTemp
   xtimedate += 3600*24
   print int(xtimedate)
   print time.localtime(xtimedate)
   r.lpush("poolTemp:history", str(randomishTemp) + ":" + str(xtimedate)  )
