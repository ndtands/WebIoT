#author :  Nguyen Duy Tan
#gmail: ndtan.hcm@gmail.com

import random
import paho.mqtt.client as mqtt
import _thread, json
from datetime import datetime
import time
import serial
temp=[0,0,0,0,0,0,0]
#====================================================
# MQTT Settings
MQTT_Broker = "192.168.0.46"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_SenSor = "Sensor"

def on_connect(client, userdata,flags, rc):
        if rc != 0:
                pass
                print ("Unable to connect to MQTT Broker...")
        else:
                print ("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
        pass

def on_disconnect(client, userdata, rc):
        if rc !=0:
                pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
client.loop_start()

def publish_To_Topic(topic, message):
        client.publish(topic,message)
        print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
#       print  ("-------------------END-----------------")

def Read_Uart_Publish():
                        temp[1]=random.randrange(60,100,1);
                        temp[0]=random.randrange(25,30,1);
                        temp[2]=random.randrange(1000,1200,5);
                        temp[3]=random.randrange(5,9,1);
                        temp[4]=random.randrange(220,250,5);
                #       temp[5]=random.randrange(25,30,1);
                        print("\n------------------------DATA RECEIVER--------------------------")
                        print("Do am:       ",temp[1],"%")
                        print("Nhiet Do:    ",temp[0],"°C")
                        print("Anh sang:    ",temp[2],"Lux")
                        print("Do PH:       ",temp[3],"pH")
                        print("Do dan dien: ",temp[4],"mS/cm")
                #       print("Temp Water:  ",temp[5],"°C")

                        Sensor_data ={}
                        Sensor_data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S")
                        Sensor_data['Hud'] = temp[1]
                        Sensor_data['Temp'] = temp[0]
                        Sensor_data['Light'] = temp[2]
                        Sensor_data['PH'] = temp[3]
                        Sensor_data['EC'] = temp[4]

                        print("\n------------------------DATA PUBLISH--------------------\n")
                        Sensor_json_data = json.dumps(Sensor_data)
                        publish_To_Topic(MQTT_Topic_SenSor, Sensor_json_data)

def thread_Read_Publish():
        while True:
                Read_Uart_Publish();
                time.sleep(5)
				pass
try:
	_thread.start_new_thread( thread_Read_Publish,( ))
except:
   print ("Error: unable to start thread")

while 1:
        pass