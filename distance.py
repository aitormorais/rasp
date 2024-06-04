import time
import requests
import RPi.GPIO as GPIO
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

url = 'https://corlysis.com:8086/write'
params = {"db": "distancias", "u": "token", "p": "813b9b7719be9606b759f1dbcef2bbd7"}
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

def enviar_datos(distance, atras):
    payload = f'distancias,distance={distance} value={atras}'
    try:
        r = requests.post(url, params=params, data=payload)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error al enviar datos: {e}')

def medir_distancia(sensor):
    try:
        return int(sensor.get_distance())
    except Exception as e:
        print(f'Error al medir distancia: {e}')
        return -1  # valor de error

def main():
    sensor_adelante = GroveUltrasonicRanger(16)
    sensor_atras = GroveUltrasonicRanger(18)
    estados = {"lejos": True, "medio": True, "cerca": True, "l": True, "m": True, "c": True}

    while True:
        distance = medir_distancia(sensor_adelante)
        atras = medir_distancia(sensor_atras)
        
        if distance == -1 or atras == -1:
            continue
        
        if distance >= 30 and estados["lejos"]:
            print('lejos Adelante')
            print(f'{distance} cm')
            estados["lejos"], estados["medio"], estados["cerca"] = False, True, True
            enviar_datos(distance, atras)
        
        if 6 <= distance < 30 and estados["medio"]:
            print('cerca Adelante')
            print(f'{distance} cm')
            estados["medio"], estados["lejos"], estados["cerca"] = False, True, True
            enviar_datos(distance, atras)
        
        if distance <= 5 and estados["cerca"]:
            print('muy cerca Adelante')
            print(f'{distance} cm')
            estados["cerca"], estados["medio"], estados["lejos"] = False, True, True
            enviar_datos(distance, atras)
            GPIO.output(24, True)
            time.sleep(1)
            GPIO.output(24, False)
            time.sleep(1)
        
        if atras >= 30 and estados["l"]:
            print('Atras lejos')
            print(f'{atras} cm')
            estados["l"], estados["m"], estados["c"] = False, True, True
            enviar_datos(distance, atras)
        
        if 6 <= atras < 30 and estados["m"]:
            print('Atras cerca')
            print(f'{atras} cm')
            estados["m"], estados["l"], estados["c"] = False, True, True
            enviar_datos(distance, atras)
        
        if atras <= 5 and estados["c"]:
            print('Atras muy cerca')
            print(f'{atras} cm')
            estados["c"], estados["m"], estados["l"] = False, True, True
            enviar_datos(distance, atras)
        
        time.sleep(1)

if __name__ == '__main__':
    main()

