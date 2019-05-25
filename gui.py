import requests
import json
from tkinter import *
import time
import datetime
import serial

window = Tk()

toggle = IntVar()

window.title("HealthVision")

light_text = ""

def checkToggle():
    try:
        if toggle.get():
            led_url = "https://api.particle.io/v1/devices/3b003b000847373336323230/led"
            data ={
                'access_token': '86928f56a4820739bd1ed711fe46d84dfb90451d',
                'args':'ON'}
            r2 = requests.post(led_url, data)
            print(r2.text)
            
        else:
            led_url = "https://api.particle.io/v1/devices/3b003b000847373336323230/led"
            data ={
                'access_token': '86928f56a4820739bd1ed711fe46d84dfb90451d',
                'args':'OFF'}
            r2 = requests.post(led_url, data)
            print(r2.text)
    except:
        print("Error: Could not post to the particle api for the LED function!")
        
def getTime():
    try:
        global time1
        time2 = time.strftime('%H:%M:%S')
        if time2 != time1:
            time1 = time2
        window.after(100, tick)
        return time1;
    except:
        return "Error"
     
def getLight():
    try:
        light_url = "https://api.particle.io/v1/devices/3b003b000847373336323230/light?access_token=86928f56a4820739bd1ed711fe46d84dfb90451d"
        r = requests.get(light_url)
        json_light = r.json()
        return json_light['result']
    except:
        print("Could not fetch light data!!!")
        return "N/A"
        
def getPulse():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        line = re.sub("[^0-9]", "", str(ser.readline()))
		##Change value to 150 or above for possible alerts
        if int(line)>10:
            led_url = "https://api.particle.io/v1/devices/3b003b000847373336323230/led"
            data ={
                'access_token': '86928f56a4820739bd1ed711fe46d84dfb90451d',
                'args':'blink'}
            r2 = requests.post(led_url, data)
            print(r2.text)
        return str(line)
    except:
        print("Could not listen to the pulse sensor reading!!!")
        return "N/A"

while True:
    Logo = Label(window, text="HealthVision", font=("Arial Bold", 24))
    Logo.grid(column=0, row=0)


    Time = Label(window, text=datetime.datetime.now().strftime('%H:%M:%S'), font=("Arial Bold", 24))
    Time.grid(column=0, row=1)
    lightcheck = Checkbutton(text='Light', variable=toggle, command=checkToggle)

    lightcheck.grid(column=0, row=2)


    lightlbl = Label(window, text="Light: "+getLight())
    lightlbl.grid(column=0, row=3)
    pulselbl = Label(window,text="Pulse: "+getPulse())
    pulselbl.grid(column=0, row=4)
    window.update()

window.protocol("WM_DELETE_WINDOW",window.destroy())
window.mainloop()
