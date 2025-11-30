from blynk import Blynk
import network
import json
import dht
import time
from machine import Pin
from umqtt.simple import MQTTClient

#Declaro as variáveis, sensores e pins.

sensor = dht.DHT22(Pin(13))
led_fisico = Pin(21, Pin.OUT)
led_fisico.off()
temp_max = 40.0
umid_min = 45.0

#começo fazendo as configurações do wifi.

wifi_ssid = "Wokwi-GUEST"
wifi_password = ""

# CONFIG DO MQTT/BLYNK
broker = "blynk.cloud"
auth_token = "ES1L-O805pabrJkvDIZGsY6ry-c6s3SP"
topic = b"pucpr/s8"

#Fazendo a conexão ao wifi
print("Conectando-se ao Wi-Fi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)

print("Conexão feita com sucesso!", sta_if.ifconfig())

#Criando mqtt cliente
cid = b"ESP32" + str(int(time.time()*1000)).encode()
c = MQTTClient(cid, broker, port=1883, user=b"device", password=auth_token.encode(), keepalive=45)
c.connect()
print("MQTT Broker conectado!")

#Fazendo a conexão ao MQTT

while True:
    print("Loop iniciando...")
    sensor.measure()
    temp = sensor.temperature()
    umid = sensor.humidity()
    print("Temperatura:", temp, "°C  Umidade:", umid)
    c.publish("ds/Temperatura", str(temp))
    c.publish("ds/Umidade", str(umid))


    # ATUALIZA O LED
    if temp <= temp_max and umid >= umid_min:
        led_fisico.off()
    else:
        led_fisico.on()

    # publica quando atingido
    if temp > temp_max or umid < umid_min:
        c.publish("ds/LED1", "1")
    else:
        c.publish("ds/LED1", "0")

    time.sleep(10)