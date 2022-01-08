import time
import requests
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
url = 'https://corlysis.com:8086/write'
params = {"db": "distancia", "u": "token", "p": "813b9b7719be9606b759f1dbcef2bbd7"}
def main():
 # Grove - Ultrasonic Ranger connected to port D16
 sensor = GroveUltrasonicRanger(16)
 sensoratras = GroveUltrasonicRanger(18)
 lejos=True
 medio=True
 cerca=True
 l=True
 m=True
 c=True
 i=0
 while True:
     distance = int(sensor.get_distance())
     atras = int(sensoratras.get_distance())
     i=i+1
     if distance >= 30 and lejos:
         print('lejosa')
         print('{} cm'.format(distance))
         lejos=False
         if not medio:
             medio=True
         if not cerca:
             cerca=True
        
         payload = 'distancias,distance=bad'+ ' value=' + str(atras)
         r= requests.post(url,params=params,data=payload)
        
     if distance >=6 and distance <30 and medio:
         print('cercaa')
         print('{} cm'.format(distance))
         medio=False
         if not lejos:
             lejos=True
         if not cerca:
             cerca=True
        
         payload = 'distancias,distance=bad'+ 'value='+ str(atras)
         r= requests.post(url,params=params,data=payload)
     if distance <= 5 and cerca:
         print('muy cercaa')
         print('{} cm'.format(distance))
         cerca=False
         if not medio:
             medio=True
         if not lejos:
             lejos=True
        
         payload = 'distancias,distance=bad'+ 'value='+ str(atras)
         r= requests.post(url,params=params,data=payload)
     if atras >= 30 and l:
         print('lejos')
         print('{} cm'.format(atras))
         l=False
         if not m:
             m=True
         if not c:
             c=True
         payload = 'distancias,distance=bad'+ 'value='+ str(atras)
         r= requests.post(url,params=params,data=payload)
     if atras >=6 and atras <30 and m:
         print('cerca')
         print('{} cm'.format(atras))
         m=False
         if not l:
             l=True
         if not c:
             c=True
         payload = 'distancias,distance=bad'+ 'value='+ str(atras)
         r= requests.post(url,params=params,data=payload)
     if atras <= 5 and c:
         print('muy cerca')
         print('{} cm'.format(atras))
         c=False
         if not m:
             m=True
         if not l:
             l=True
         payload = 'distancias,distance=bad'+ 'value='+ str(atras)
         r= requests.post(url,params=params,data=payload)
    
    
    
time.sleep(1)

if __name__ == '__main__':
 main()
