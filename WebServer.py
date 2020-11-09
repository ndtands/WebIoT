"""
author: Sang 
"""

# importing libraries 
import tkinter as tk
from tkinter import ttk
from tkinter import *

import PIL
from PIL import ImageTk, Image

from datetime import datetime
import pytz

from urllib.request import urlopen
import json

import paho.mqtt.client as mqtt

from tkinter import filedialog
from tkfilebrowser import askopendirname, askopenfilenames, asksaveasfilename
from tkinter import scrolledtext    
import os

win = tk.Tk() 
win.title("Iot Program")
# win.resizable(0 , 0 )  # preventing it from being resizable 

tab_control = ttk.Notebook(win) # 1st, create control Tab using Notebook

tab1 = ttk.Frame(tab_control) # 2nd, create Tabs using  
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Sensor') # 3rd, add Tabs to control tab
tab_control.add(tab2, text='Image')
tab_control.add(tab3, text='Weather')

tab_control.pack(expand = 1, fill ="both") # 4rd, Package to display  


# TAB1: SENSOR
class ReadingMeter:
    def __init__(self, x, y, name,unit):
        self.reading = DoubleVar()
        var_name = Label(tab1, text = name, font =("consolas", 13, "bold"))
        var_unit = Label(tab1, text = unit, font =("consolas", 13, "bold"))
        self.display = Label(tab1, textvariable=self.reading, relief = "solid", borderwidth = 0.5, font = "Times 13")  # we need this Label as a variable
        self.display.place(x = x+85, y = y, width = 100)
        var_name.place(x = x, y=y)
        var_unit.place(x = x+200, y = y )

class DateTime:
    def __init__(self, x, y, name):
        self.reading = DoubleVar()
        var_name = Label(tab1, text = name,font =("consolas", 13, "bold"))
        self.display = Label(tab1, textvariable=self.reading, font =("consolas", 13, "bold"))  # we need this Label as a variable
        self.display.place(x = x+60, y = y, width = 200)
        var_name.place(x = x, y = y)


MQTT_Topic= "Sensor"
# Hàm cập nhật giá trị
def Sensor_Data_Handler(jsonData):
    json_Dict = json.loads(jsonData)
    PH = json_Dict['PH']
    Humidity = json_Dict['Hud']
    EC = json_Dict['EC']
    Light = json_Dict['Light']
    # Date = json_Dict['Date']
    Temperature = json_Dict['Temp']
    # Pump1 = json_Dict['NuA']
    # Pump2 = json_Dict['NuB']
    # Water = json_Dict['WIn']
    garden_Temperature.reading.set(Temperature)
    garden_PH.reading.set(PH)
    garden_EC.reading.set(EC)
    garden_Humidity.reading.set(Humidity)
    garden_Light.reading.set(Light)
    # garden_Date.reading.set(Date)
    # garden_Pump1.reading.set(Pump1)
    # garden_Pump2.reading.set(Pump2)
    # garden_Water.reading.set(Water)
# Hàm phân loại topic
def update_meters(topic, value):
    if topic == "Sensor":
        Sensor_Data_Handler(value)
# Hàm publish messages
def Pulish_To_Topic(topic, message1,message2, message3):
    message_dict = {}
    message_dict['Control_Pump1'] = message1
    message_dict['Control_Pump2'] = message2
    message_dict['Control_Water'] = message3
    message_dict['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S")
    message_json = json.dumps(message_dict)
    client.publish(topic,message_json)
    print("Published:" + str(message_json) + " " + "on MQTT Topic: " + str(topic))


# Lấy giá trị trong khung nhập liệu và publish
# def send_message1( en1,en2):
#     msg1 = en1.get()
#     msg2 = en2.get()
#     msg3 = 'u'
#     if msg1 == '' :
#         msg1 = 0    
#     if msg2 == '' :
#         msg2 = 0
#     Pulish_To_Topic(MQTT_Topic_Temperature,msg1,msg2,msg3)
# def send_message2(en3):
#     msg1 = 'u'
#     msg2 = 'u'
#     msg3 = en3.get()
#     Pulish_To_Topic(MQTT_Topic_Temperature,msg1,msg2,msg3) 

# Hàm exit
def quit_program(client):
    client.loop_stop()
    client.disconnect()
    print("Closed connection")
    exit()

def on_connect(client, userdata, flags, rc):
    if rc == 0 :
        status_data.set("Connected")
    else :
        status_data.set("Not Connected")
    print("Connected With Result Code "+str(rc))
    print("Connecting to MQTT BROKER : {}".format(MQTT_Broker))

def on_message(client, userdata, message):
    print(message.topic + " Received: " + message.payload.decode())
    update_meters(message.topic, message.payload.decode())

def on_publish(client, userdata, rc):
    pass

# Establishing Connection
MQTT_Broker = "192.168.100.8"
MQTT_Port = 1883

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_Broker, MQTT_Port)

client.subscribe("Sensor", qos=1)


# Khung hiển thị

garden_Temperature = ReadingMeter(550, 50, "Temp","Celcius")
garden_PH = ReadingMeter(550, 80, "PH","pH")
garden_Humidity = ReadingMeter(550, 110, "Humidity","%")
garden_EC = ReadingMeter(550, 140, "EC","mS/cm")
garden_Light = ReadingMeter(550, 170, "Light","Lux")
garden_Pump1 = ReadingMeter(200, 50, "","l")
garden_Pump2 = ReadingMeter(200, 80, "","l")
garden_Water = ReadingMeter(200, 110, "","l")

# Tạo các Label
lb1 = Label (tab1, text = "Set", font =("consolas", 14, "bold"))
lb1.place (x = 145, y=10)
lb2 = Label (tab1, text = "Pumped", font =("consolas", 14, "bold"))
lb2.place (x = 310, y=10)
lb3 = Label (tab1, text = "Nutrition A", font =("consolas", 13, "bold"))
lb3.place (x = 6, y=50)
lb4 = Label (tab1, text = "l",font =("consolas", 13, "bold"))
lb4.place (x = 210, y=50)
lb5 = Label (tab1, text = "Nutrition B", font =("consolas", 13, "bold"))
lb5.place (x = 6, y=80)
lb6 = Label (tab1, text = "l",font =("consolas", 13, "bold") )
lb6.place (x = 210, y=80)
lb7 = Label (tab1, text = "Water In", font =("consolas", 13, "bold") )
lb7.place (x = 6, y=110)
lb8 = Label (tab1, text = "l" ,font =("consolas", 13, "bold"))
lb8.place (x = 210, y=110)

# Khung nhập số liệu
en1 = Entry(tab1, font = "Times 13")
en1.place (x = 125, y=50, width = 80 )
en2 = Entry(tab1, font = "Times 13")
en2.place (x = 125, y=80, width = 80 ) 
en3 = Entry(tab1, font = "Times 13")
en3.place (x = 125, y=110, width = 80 )

# Button
bt1 = Button(tab1, text = "PUMB NUTRITION", font = ("consolas", 14, "bold"), bg = "cyan", fg = "white")
bt1.place(x = 80, y = 180, width = 170, height = 30)
bt1['command'] = lambda : send_message1( en1,en2) 
bt2 = Button(tab1, text = "PUMP WATER", font = ("consolas", 14, "bold"), bg = "cyan", fg = "white")
bt2.place(x = 270, y = 180, width = 120, height = 30)
bt2['command'] = lambda : send_message2(en3)
q_button = Button(tab1, text = "Exit", font = ("consolas",14,"bold"), bg = "cyan", fg = "white")
q_button.place(x = 20, y= 350 , width = 120 , height = 30)
q_button['command'] = lambda: quit_program(client)

# Date_time
garden_Date = DateTime(250, 350, "Date: ")
# Status
status_data = DoubleVar()
status = Label (tab1, textvariable = status_data,  font =("consolas", 13, "bold") )
status.place(x= 700 , y =350)
status_label = Label (tab1, text = 'Status: ', font =("consolas", 13, "bold") )
status_label.place(x = 610 , y = 350)

status_data = DoubleVar()
status = Label (tab1, textvariable = status_data,  font =("consolas", 13, "bold") )
status.place(x= 700 , y =350)
status_label = Label (tab1, text = 'Status: ', font =("consolas", 13, "bold") )
status_label.place(x = 610 , y = 350)

client.loop_start()


# TAB2: IMAGE
def c_open_file_old():
    rep = filedialog.askopenfilenames(parent=tab2, initialdir='/', initialfile='tmp',
                                      filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*")])
    print(rep)


def c_open_dir_old():
    rep = filedialog.askdirectory(parent=tab2, initialdir='/tmp')
    print(rep)


def c_save_old():
    rep = filedialog.asksaveasfilename(parent=tab2, defaultextension=".png", initialdir='/tmp', initialfile='image.png',
                                       filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*")])
    print(rep)
def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
def open_img1():
    x1 = openfn()
    img1 = Image.open(x1)
    img1 = img1.resize((220, 220), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(img1)
    panel = Label(tab2, image=img1)
    panel.image = img1
    panel.grid(column=1, row=0, rowspan = 5)
def open_img2():
    x2 = openfn()
    img2 = Image.open(x2)
    img2 = img2.resize((220, 220), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    panel = Label(tab2, image=img2)
    panel.image = img2
    panel.grid(column=1, row=5, rowspan = 5)
def open_img3():
    x3 = openfn()
    img3 = Image.open(x3)
    img3 = img3.resize((220, 220), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img3)
    panel = Label(tab2, image=img3)
    panel.image = img3
    panel.grid(column=1, row=11, rowspan = 5)
def changenotea1():
    text1.configure(state= 'normal')
    framea21 = Frame(tab2)
    changebtna21 = Button(framea21, text ="SAVE" ,command = changenotea2, bg = "dark green", fg = "white", font="Lucid 15" )
    changebtna21.grid(row = 2, column =3, ipadx = 95, ipady =5)
    framea21.grid(row =2 , column =3, padx =20)
def changenotea2():    
    text1.configure(state= 'disabled')
    framea22 = Frame(tab2)
    changebtna22 = Button(framea22, text ="Change note", command = changenotea1, bg = "light green", fg = "black", font="Lucid 15" )
    changebtna22.grid(row = 2, column =3, ipadx = 67, ipady =5)
    framea22.grid(row =2 , column =3, padx =20)

def changenoteb1():
    text2.configure(state= 'normal')
    frameb21 = Frame(tab2)
    changebtnb21 = Button(frameb21, text ="SAVE" ,command = changenoteb2, bg = "dark green", fg = "white", font="Lucid 15" )
    changebtnb21.grid(row = 7, column =3, ipadx = 95, ipady =5)
    frameb21.grid(row =7 , column =3, padx =20)
def changenoteb2():    
    text2.configure(state= 'disabled')
    frameb22 = Frame(tab2)
    changebtnb22 = Button(frameb22, text ="Change note" , command = changenoteb1, bg = "light green", fg = "black", font="Lucid 15" )
    changebtnb22.grid(row = 7, column =3, ipadx = 67, ipady =5)
    frameb22.grid(row =7 , column =3, padx =20)

def changenotec1():
    text3.configure(state= 'normal')
    framec21 = Frame(tab2)
    changebtnc21 = Button(framec21, text ="SAVE" ,command = changenotec2, bg = "dark green", fg = "white", font="Lucid 15" )
    changebtnc21.grid(row = 12, column =3, ipadx = 95, ipady =5)
    framec21.grid(row =12 , column =3, padx =20)
def changenotec2():    
    text3.configure(state= 'disabled')
    framec22 = Frame(tab2)
    changebtnc22 = Button(framec22, text ="Change note" , command = changenotec1,  bg = "light green", fg = "black", font="Lucid 15" )
    changebtnc22.grid(row = 12, column =3, ipadx = 67, ipady =5)
    framec22.grid(row =12 , column =3, padx =20)


path1 = 'image1.jpg'
img1 = Image.open(path1)
img1 = img1.resize((220, 220), Image.ANTIALIAS)
photo1= ImageTk.PhotoImage(img1)
panel1 = ttk.Label(tab2, image = photo1)
panel1.grid(row = 0, column = 1, padx=10, pady=3, sticky = tk.W, rowspan =5)

path2 = 'image2.jpg'
img2 = Image.open(path2)
img2 = img2.resize((220, 220), Image.ANTIALIAS)
photo2= ImageTk.PhotoImage(img2)
panel2 = ttk.Label(tab2, image = photo2)
panel2.grid(row = 5, column = 1,padx=10, pady=3, sticky = tk.W, rowspan =5)

path3 = 'image3.jpg'
img3 = Image.open(path3)
img3 = img3.resize((220, 220), Image.ANTIALIAS)
photo3= ImageTk.PhotoImage(img3)
panel3 = ttk.Label(tab2, image = photo3)
panel3.grid(row = 11, column = 1, padx=10, pady=3, sticky = tk.W, rowspan =5)

# //------------------------------------------------------------------------------------------------------------
txtfont= ('bold', 18)
text1 = scrolledtext.ScrolledText(tab2, width=22, height=5, font= txtfont)
text1.insert(INSERT,'Time: 4days, 2h, 30m\nNote: Normal\nCategory: Daily Image')
text1.grid(column=2, row=0, padx = 10, pady = 5, rowspan =3)
text1.configure(state= 'disabled')

framex = Frame(tab2)
dataxbtnc = Button(framex, text ="Upload Image" , command=open_img1, bg = "light blue", fg = "black", font="Lucid 18 italic", relief ="groove" )
dataxbtnc.grid(row = 3, column =2, ipadx = 77, ipady =3)
framex.grid(row = 3, column = 2, padx = 10, pady = 3)


text2 = scrolledtext.ScrolledText(tab2, width=22, height=5, font= txtfont)
text2.insert(INSERT,'Time: 5days, 1h, 12m\nNote: Normal Leaf\nCategory: Daily Image')
text2.grid(column=2, row=5, padx = 10, pady = 5, rowspan =3)
text2.configure(state= 'disabled')

framey = Frame(tab2)
dataybtnc = Button(framey, text ="Upload Image" , command=open_img2,bg = "light blue", fg = "black", font="Lucid 18 italic" ,relief ="groove")
dataybtnc.grid(row = 8, column =2, ipadx = 77, ipady =3 )
framey.grid(row = 8, column = 2, padx = 10, pady = 3)

text3 = scrolledtext.ScrolledText(tab2, width=22, height=5, font= txtfont)
text3.insert(INSERT,'Time: 10days, 5h, 52m\nNote: Need to pump water\nCategory: Daily Image')
text3.grid(column=2, row=10, padx = 10, pady = 5, rowspan =3)
text3.configure(state= 'disabled')


framez = Frame(tab2)
datazbtnc = Button(framez, text ="Upload Image" , command=open_img3, bg = "light blue", fg = "black", font="Lucid 18 italic", relief ="groove" )
datazbtnc.grid(row = 13, column =2, ipadx = 77, ipady =3)
framez.grid(row = 13, column = 2, padx = 10, pady = 3)


# //-----------------------------------------------------------------------------------------------------------
framea1 = Frame(tab2)
uploadbtna = Button(framea1, text ="Upload Document" , command=c_open_file_old, bg = "light green", fg = "black", font="Lucid 15" )
uploadbtna.grid(row = 1, column =3, ipadx = 45, ipady =5 )
framea1.grid(row =1 , column =3, padx = 5,)

framea2 = Frame(tab2)
changebtna = Button(framea2, text ="Change note" ,command =changenotea1 ,bg = "light green", fg = "black", font="Lucid 15" )
changebtna.grid(row = 2, column =3, ipadx = 67, ipady =5)
framea2.grid(row =2 , column =3, )

framea3 = Frame(tab2)
dcmtbtna = Button(framea3, text ="Document" , command=c_save_old, bg = "light green", fg = "black", font="Lucid 15" )
dcmtbtna.grid(row = 3, column =3, ipadx = 79, ipady =5 )
framea3.grid(row =3 , column =3)
# //-----------------------------------------------------------------------------------------------------------
frameb1 = Frame(tab2)
uploadbtnb = Button(frameb1, text ="Upload Document" , command=c_open_file_old, bg = "light green", fg = "black", font="Lucid 15" )
uploadbtnb.grid(row = 6, column =3, ipadx = 45, ipady =5 )
frameb1.grid(row = 6, column =3, padx = 20)

frameb2 = Frame(tab2)
changebtnb = Button(frameb2, text ="Change note" , command = changenoteb1, bg = "light green", fg = "black", font="Lucid 15" )
changebtnb.grid(row = 7, column =3, ipadx = 67, ipady =5 )
frameb2.grid(row = 7, column =3, padx = 20)

frameb3 = Frame(tab2)
dcmtbtnb = Button(frameb3, text ="Document" , command=c_save_old, bg = "light green", fg = "black", font="Lucid 15" )
dcmtbtnb.grid(row = 8, column =3, ipadx = 79, ipady =5 )
frameb3.grid(row = 8, column =3, padx = 20)
# //-----------------------------------------------------------------------------------------------------------
framec1 = Frame(tab2)
uploadbtnc = Button(framec1, text ="Upload Document"  , command=c_open_file_old, bg = "light green", fg = "black", font="Lucid 15" )
uploadbtnc.grid(row = 11, column =3, ipadx = 45, ipady =5 )
framec1.grid(row = 11, column =3, padx =20 )

framec2 = Frame(tab2)
changebtnc = Button(framec2, text ="Change note" ,command = changenotec1, bg = "light green", fg = "black", font="Lucid 15" )
changebtnc.grid(row = 12, column =3, ipadx = 67, ipady =5 )
framec2.grid(row = 12, column =3, padx = 20)

framec3 = Frame(tab2)
dcmtbtnc = Button(framec3, text ="Document" , command=c_save_old,  bg = "light green", fg = "black", font="Lucid 15" )
dcmtbtnc.grid(row = 13, column =3, ipadx = 79, ipady =5 )
framec3.grid(row = 13, column =3, padx =20 )

# //----------------------------------------------------------------------------------------------

labeld = Label(tab2, text ="Ho Chi Minh City\n Startday: 30/04/2018\n IN PROGRESS", fg = "black",font ="Cooper 20 bold", relief = "groove")
labeld.grid(row = 2, column =4, padx =10, pady=5, rowspan =5)

framed1 = Frame(tab2)
databtnc = Button(framed1, text ="Collected Data" , command=c_open_dir_old, bg = "light blue", fg = "black", font="Lucid 20" )
databtnc.grid(row = 7, column =4 )
framed1.grid(row = 7, column = 4, padx = 10, pady = 5 )


# TAB3: WEATHER 
"""creating a labelframe inside `tab3`
This will allow the user to enter the city name . """

weatherCitiesFrame = ttk.LabelFrame(tab3 , text = "  Latest Observation for   "  )
weatherCitiesFrame.grid(row = 0 , column = 0 , padx = 8 , pady = 4 )

"""creating another labelframe inside `tab3`  
    Here all the weather related details will appear . 
"""

weatherConditionsFrame = ttk.LabelFrame(tab3 , text = "  Current Weather Conditions "  )
weatherConditionsFrame.grid(row = 1 , column = 0 , padx = 2 , pady = 12 )

# adding widgets to the labelframe  `weatherCitiesFrame` we created 

ttk.Label(weatherCitiesFrame , text = "City: " ).grid(row = 0 , column = 0  )
city = tk.StringVar() # for storing the value of city

citySelected = ttk.Combobox(weatherCitiesFrame , width =24 , textvariable = city )
citySelected["values"] = ('Thanh pho Ho Chi Minh, VN', 'My Tho, VN', 'Ha Tinh, VN')
citySelected.current(0)
citySelected.grid(row = 0 , column = 1 )

#------------------------------------
# Here , This will show city and countrycode of the city selected for which the weather is displayed . 

location = tk.StringVar()
ttk.Label(weatherCitiesFrame , textvariable = location ).grid(row = 1 , column = 1 , columnspan = 2 )

#----------------------------------

#--------------------------------
# callback function to get the weather details 

def getWeather() :
    cityVar = city.get() 
    getWeatherData(cityVar)

#------------------------------------------

getWeatherbtn = ttk.Button(weatherCitiesFrame , text = "Get Weather", command = getWeather )
getWeatherbtn.grid(row = 0 , column = 2 )

# ------changing the padding of our widgets inside labelframe `weatherCitiesFrame`

for child in weatherCitiesFrame.winfo_children() :
    child.grid_configure(padx = 5, pady = 2 )

#------------------------------

ENTRY_WIDTH = 24

# Adding Label and entrybox widgets to labelFrame `weatherConditionsFrame`

ttk.Label(weatherConditionsFrame , text = "Last Updated:").grid(row = 1 , column = 0 , sticky = tk.E)
updated = tk.StringVar()
updatedEntry = ttk.Entry(weatherConditionsFrame , width = ENTRY_WIDTH , textvariable = updated , state = "readonly" , foreground = "#1F22D3" )
updatedEntry.grid(row = 1 , column = 1 ,sticky = tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame , text = "Weather:" ).grid(row = 2 , column = 0 , sticky = tk.E)
weather = tk.StringVar()
weatherEntry = ttk.Entry(weatherConditionsFrame , width = ENTRY_WIDTH , textvariable =weather , state = "readonly" , foreground = "#1F22D3")
weatherEntry.grid(row = 2 , column = 1 , sticky = tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame , text = "Temperature:").grid(row = 3 , column = 0 , sticky =tk.E)
temp = tk.StringVar()
tempEntry = ttk.Entry(weatherConditionsFrame , width = ENTRY_WIDTH , textvariable = temp , state = "readonly", foreground = "#1F22D3")
tempEntry.grid(row = 3 , column = 1 , sticky = tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame , text ="Relative Humidity:").grid(row = 4 , column = 0 , sticky = tk.E)
relHumidity = tk.StringVar()
relHumidityEntry = ttk.Entry(weatherConditionsFrame , width = ENTRY_WIDTH , textvariable = relHumidity , state = "readonly", foreground = "#1F22D3")
relHumidityEntry.grid(row = 4 , column = 1 , sticky = tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame, text="Wind:").grid( row= 5 ,column = 0 , sticky= tk.E)
wind = tk.StringVar()
windEntry = ttk.Entry(weatherConditionsFrame, width=ENTRY_WIDTH, textvariable=wind, state='readonly', foreground = "#1F22D3")
windEntry.grid( row=5, column = 1 ,  sticky=tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame, text="Visibility:").grid( row=6,column = 0 , sticky= tk.E)
visi = tk.StringVar()
visiEntry = ttk.Entry(weatherConditionsFrame, width=ENTRY_WIDTH, textvariable=visi, state='readonly' , foreground = "#1F22D3")
visiEntry.grid( row=6, column = 1 , sticky= tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame, text="Pressure:").grid( row=7,column = 0 , sticky= tk.E)
pressure = tk.StringVar()
pressureEntry = ttk.Entry(weatherConditionsFrame, width=ENTRY_WIDTH, textvariable=pressure, state='readonly' , foreground = "#1F22D3")
pressureEntry.grid( row=7, column = 1 ,  sticky= tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame, text="Sunrise:").grid( row=8 , column = 0 , sticky= tk.E)
sunrise = tk.StringVar()
sunriseEntry = ttk.Entry(weatherConditionsFrame, width=ENTRY_WIDTH, textvariable=sunrise, state='readonly' , foreground = "#1F22D3")
sunriseEntry.grid( row=8, column = 1 ,  sticky= tk.W)
#---------------------------------------------
ttk.Label(weatherConditionsFrame, text="Sunset:").grid( row=9, column = 0 , sticky= tk.E)
sunset = tk.StringVar()
sunsetEntry = ttk.Entry(weatherConditionsFrame, width=ENTRY_WIDTH, textvariable=sunset, state='readonly' , foreground = "#1F22D3")
sunsetEntry.grid( row=9, column = 1 ,  sticky= tk.W)
#---------------------------------------------


#------ changing the padding of our widgets inside labelframe `weatherConditionsFrame`

for child in weatherConditionsFrame.winfo_children() : 
    child.grid_configure(padx = 14 , pady = 5 )


#---------------------------------------------

"""OpenWeatherMap data collection """

#------- open weather map api key 
OWM_API_KEY = 'd3bcf629aff3c1ef4a8e10deecd36eb5'
#--------------
def getWeatherData(city = "London,uk") :
    city = city.replace(' ', '%20')
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, OWM_API_KEY) 
    response = urlopen(url)
    data = response.read().decode()
    jsonData = json.loads(data)

    # --------------------------------
    """
    from pprint import pprint
    pprint(jsonData) 

    This will print the fetched json data to the console 
    uncomment above lines to see how the fetched json data looks like . 

    """
    #---------------------------------

    dateTimeUnix = jsonData["dt"]     # unix timestamp 
    humidity = jsonData['main']['humidity']
    pressr = jsonData["main"]["humidity"]
    tempKelvin = jsonData['main']['temp']
    cityName = jsonData["name"]
    countryName = jsonData["sys"]["country"]
    sunriseUnix = jsonData["sys"]["sunrise"]  # unix timestamp 
    sunsetUnix = jsonData["sys"]["sunset"]   # unix timestamp 
    try :
        visibility = jsonData["visibility"]    # in case visibility is not provided in the fetched data
    except :
        visibility = 'N/A'
    
    weatherDesc = jsonData['weather'][0]['description']
    weatherIcon = jsonData['weather'][0]['icon']
    windDeg = jsonData['wind']['deg']
    windSpeed = jsonData['wind']['speed']

    def kelvinToCelsius (tempK) :
        return "{:.1f}".format(tempK - 273.15 )

    def kelvinToFahrenheit ( tempK) :
        return "{:.1f}".format((tempK - 273.15)* 1.8 + 32)

    
    # we need pytz to provide details about the timezone of the city while converting date from unixtimestamp to datetime 

    #----Helper function to convert unixtimestamp to Datetime -------------

    def unixToDatetime (unixTime) :
        return datetime.fromtimestamp(int(unixTime ), tz= pytz.FixedOffset(int(jsonData["timezone"]) / 60) ).strftime('%Y-%m-%d  %H:%M:%S')

        # jsonDate["timezone"] stores the timezone of the city ( in seconds ) .
        #  Divide it by 60 to get timezone in minutes . 
    #-------------------------------

    def meterToMiles(meter ) :
        return "{:.2f}".format((meter * 0.00062137))
    
    if ( visibility  == 'N/A') :
        visibilityMiles = "N/A"
    else :
        visibilityMiles = meterToMiles(visibility)

    
    def mpsTomph (meterSecond) :
        return "{:.1f}".format((meterSecond) * (2.23693629))

    location.set("{},{}".format(cityName , countryName))
    updated.set(unixToDatetime(dateTimeUnix))
    weather.set(weatherDesc)
    
    tempC = kelvinToCelsius(tempKelvin)
    tempF = kelvinToFahrenheit(tempKelvin)
    temp.set("{} \xb0F  ({} \xb0C )".format(tempF , tempC ) )

    relHumidity.set("{} %".format(humidity) ) 

    windSpeed = mpsTomph(windSpeed)
    wind.set("{} degrees at {} MPH".format(windDeg , windSpeed))

    visi.set("{} miles ".format(visibilityMiles))

    pressure.set("{} hPa".format(pressr))

    sunrise.set(unixToDatetime(sunriseUnix))
    sunset.set(unixToDatetime(sunsetUnix))

    #--------- To display weather icon ----------------

    urlIcon = "http://openweathermap.org/img/w/{}.png".format(weatherIcon)
    iconResponse = urlopen(urlIcon)
    openIm = PIL.Image.open(iconResponse )
    openPhoto = PIL.ImageTk.PhotoImage(openIm)
    imgLabel = ttk.Label(weatherCitiesFrame , image = openPhoto)
    imgLabel.image = openPhoto  # need to keep a reference of the image for images to appear,else it won't appear  . 

    imgLabel.grid(row = 1 , column = 0 )
    win.update() 

    #------------------


win.mainloop() 