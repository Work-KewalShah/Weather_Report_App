#importing necessary libraries
import datetime as dt
import requests
import tkinter as tk
import json
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#convert kelvin temperature to celcius and fahrenheit
def kelvin_to_celcius_fahrenheit(kelvin):
    celcius = kelvin-273.15
    fahrenheit = (celcius) * (9/5) + 32
    return celcius, fahrenheit

#Start button function
def proceed_F():
    if note_frame.winfo_ismapped():
        note_frame.pack_forget()
        weather_app_frame.pack(pady=10, padx=10)

#checking weather
def check_weather_F():
    #with open('api_keys.txt', 'r') as file:
        #loaded_keys = json.load(file)
    
    #weather_api_key = loaded_keys{'openweathermap'}    opening api_keys.txt and getting key from there
    
    city_zip = city_zip_E.get()
    weather_api_key = "a52e364d03edbb4f52aefa0654d87ee7"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    if city_zip.isdigit():
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city_zip)
        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            print("Location not found")
        params = {'lat': latitude, 'lon': longitude, 'exclude': 'minutely,hourly', 'appid': weather_api_key}
    else:
        params = {'q': city_zip, 'appid':weather_api_key}
        
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        if warning_L.winfo_ismapped():
            warning_L.pack_forget()
        
        global temp_kelvin
        temp_kelvin = weather_data['main']['temp']
        global temp_celcius
        global temp_fahrenheit
        temp_celcius, temp_fahrenheit = kelvin_to_celcius_fahrenheit(temp_kelvin)
        temp_celcius = str(temp_celcius)
        temp_fahrenheit = str(temp_fahrenheit)
        global humidity
        humidity = str(weather_data['main']['humidity'])
        global wind_speed
        wind_speed = str(weather_data['wind']['speed'])
        global weather_description
        weather_description = str(weather_data['weather'][0]['description'])
        global weather_icon_id
        weather_icon_id = str(weather_data['weather'][0]['icon'])
        global city
        city = str(weather_data['name'])
        global date_time
        date_time = str(dt.datetime.utcfromtimestamp(weather_data['dt']))
        
        if report_data_frame.winfo_ismapped():
            report_data_frame.pack_forget()
            city_L.config(text=city)
            date_time_B.config(text=date_time)
            weather_description_B.config(text=weather_description)
            temp_B.config(text=temp_celcius[:5]+"°C or "+temp_fahrenheit[:5]+"°F")
            humidity_B.config(text=humidity+"%")
            wind_speed_B.config(text=wind_speed+"meter/sec")
            separator1_frame.pack(fill='x', pady=5)
            
            date_time_desc_frame.pack_forget()
            weather_description_desc_frame.pack_forget()
            temp_desc_frame.pack_forget()
            humidity_desc_frame.pack_forget()
            wind_speed_desc_frame.pack_forget()
            
            report_data_frame.pack()
        else:
            city_L.config(text=city)
            date_time_B.config(text=date_time)
            weather_description_B.config(text=weather_description)
            temp_B.config(text=temp_celcius[:5]+"°C or "+temp_fahrenheit[:5]+"°F")
            humidity_B.config(text=humidity+"%")
            wind_speed_B.config(text=wind_speed+"meter/sec")
            separator1_frame.pack(fill='x', pady=5)
            report_data_frame.pack()
    else:
        if report_data_frame.winfo_ismapped():
            report_data_frame.pack_forget()
        warning_L.config(text="Unable to recieve weather data\nEnter correct spelling or zip code")
        warning_L.pack(pady=5)

#description upon click of date time info
def date_time_F():
    if date_time_desc_frame.winfo_ismapped():
        date_time_desc_frame.pack_forget()
    else:
        date_time2_L.config(text="• Date(yyyy-mm-dd): "+date_time[:10])
        date_time3_L.config(text="• Time(hr-min-sec): "+date_time[11:])
        date_time_desc_frame.pack(side=tk.TOP, anchor="w", pady=5)

#description upon click of weather description
def weather_description_F():
    if weather_description_desc_frame.winfo_ismapped():
        weather_description_desc_frame.pack_forget()
    else:
        global icon
        icon_url = f"http://openweathermap.org/img/wn/{weather_icon_id}.png"
        icon = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
        if icon:
            weather_description1_L.config(text="Looks like "+city+" is experiencing a bit of "+weather_description)
            weather_description2_L.config(image=icon)
            weather_description_desc_frame.pack(side=tk.TOP, anchor="w", pady=5)

#description upon click of temperature
def temp_F():
    if temp_desc_frame.winfo_ismapped():
        temp_desc_frame.pack_forget()
    else:
        global normal_temp
        normal_temp = 25.0
        temp1_L.config(text=f"Normal Temperature: {normal_temp}°C")
        temp2_L.config(text=f"Retrieved Temperature: {temp_celcius[:5]}°C")
        
        plt.ioff()
        plt.figure(figsize=(4, 2.7))
        temperatures = [normal_temp, float(temp_celcius)]
        labels = ['Normal', 'Retrieved']
        plt.bar(labels, temperatures, color=['green', 'blue'])
        plt.xlabel('Temperature')
        plt.ylabel('°C')
        plt.title('Temperature Data Comparison')
        global temp_canvas
        if temp_canvas:
            temp_canvas.get_tk_widget().destroy()
        
        temp_canvas = FigureCanvasTkAgg(plt.gcf(), master=temp_desc_frame)
        temp_canvas.get_tk_widget().pack(pady=5, padx=5)
        
        plt.close()
        
        temp_desc_frame.pack()

#description upon click of humidity info
def humidity_F():
    if humidity_desc_frame.winfo_ismapped():
        humidity_desc_frame.pack_forget()
    else:
        global normal_humidity
        normal_humidity = 40
        humidity1_L.config(text=f"Normal Humidity: {normal_humidity}%")
        humidity2_L.config(text=f"Retrieved Humidity: {humidity}%")
        
        plt.ioff()
        plt.figure(figsize=(4, 2.7))
        humiditys = [normal_humidity, float(humidity)]
        labels = ['Normal', 'Retrieved']
        plt.bar(labels, humiditys, color=['green', 'blue'])
        plt.xlabel('Humidity')
        plt.ylabel('%')
        plt.title('Humidity Data Comparison')
        global humidity_canvas
        if humidity_canvas:
            humidity_canvas.get_tk_widget().destroy()
        
        humidity_canvas = FigureCanvasTkAgg(plt.gcf(), master=humidity_desc_frame)
        humidity_canvas.get_tk_widget().pack(pady=5, padx=5)
        
        plt.close()
        
        humidity_desc_frame.pack()

#description upon click of wind speed info
def wind_speed_F():
    if wind_speed_desc_frame.winfo_ismapped():
        wind_speed_desc_frame.pack_forget()
    else:
        global normal_wind_speed
        normal_wind_speed = 2.3
        wind_speed1_L.config(text=f"Normal Wind Speed: {normal_wind_speed}meter/sec")
        wind_speed2_L.config(text=f"Retrieved Wind Speed: {wind_speed}meter/sec")
        
        plt.ioff()
        plt.figure(figsize=(4, 2.7))
        wind_speeds = [normal_wind_speed, float(wind_speed)]
        labels = ['Normal', 'Retrieved']
        plt.bar(labels, wind_speeds, color=['green', 'blue'])
        plt.xlabel('Wind Speed')
        plt.ylabel('meter/sec')
        plt.title('Wind Speed Data Comparison')
        global wind_speed_canvas
        if wind_speed_canvas:
            wind_speed_canvas.get_tk_widget().destroy()
        
        wind_speed_canvas = FigureCanvasTkAgg(plt.gcf(), master=wind_speed_desc_frame)
        wind_speed_canvas.get_tk_widget().pack(pady=5, padx=5)
        
        plt.close()
        
        wind_speed_desc_frame.pack()

root = tk.Tk()
root.title("Weather Report")

#starting frame, where note is given and start button is present
note_frame = tk.Frame(root)
note_frame.pack(pady=5, padx=10)

note_heading_L = tk.Label(note_frame, text="Weather Report", font=("Calibri", 25, "bold"))
note_heading_L.pack(pady=10)

note_title_L = tk.Label(note_frame, text="Kindly take note of following points for proper working of application:", font=("Calibri", 15, "bold"))
note_title_L.pack(anchor="w")
note_content1_L = tk.Label(note_frame, text="• Make sure your system is connected to active internet connection", font=("Calibri", 12))
note_content1_L.pack(padx=10, anchor="w")
note_content2_L = tk.Label(note_frame, text="• For better results, try entering city name", font=("Calibri", 12))
note_content2_L.pack(padx=10, anchor="w")
note_content3_L = tk.Label(note_frame, text="• If encountering error, re-check spelling or zip-code entered", font=("Calibri", 12))
note_content3_L.pack(padx=10, anchor="w")
note_content4_L = tk.Label(note_frame, text="• For any queries, feel free to contact at below Email-ID", font=("Calibri", 12))
note_content4_L.pack(padx=10, anchor="w")

proceed_B = tk.Button(note_frame, text="Start", command=proceed_F, font=("Calibri", 15, "bold"))
proceed_B.pack(pady=7)

creatornote_L = tk.Label(note_frame, text="Creator: Kewal Shah\nContact: work.kewalshah@gmail.com", font=("Calibri", 8, "bold"))
creatornote_L.pack(pady=5, side=tk.BOTTOM)

#frame after clicking of Start button
weather_app_frame = tk.Frame(root)

city_zip_entry_L = tk.Label(weather_app_frame, text="Enter City Name or Zip-Code")
city_zip_entry_L.pack(padx=5, anchor="w")

city_zip_E = tk.Entry(weather_app_frame, width=70, justify=tk.CENTER)
city_zip_E.pack(padx=5, pady=5)

check_weather_B = tk.Button(weather_app_frame, text="Check Weather", command=check_weather_F, font=("Calibri", 10, "bold"))
check_weather_B.pack(pady=5)

warning_L = tk.Label(weather_app_frame, text="", fg="red", font=("Calibri", 10, "bold"))

separator1_frame = tk.Frame(weather_app_frame, height=3, bd=1, relief=tk.SUNKEN)

#Frame after clicking Check Weather
report_data_frame = tk.Frame(weather_app_frame)

city_frame = tk.Frame(report_data_frame)
city_L = tk.Label(city_frame, text="", font=("Calibri", 25, "bold"))
city_L.pack(side=tk.LEFT)
city_frame.pack(side=tk.TOP)

date_time_main_frame = tk.Frame(report_data_frame)
date_time_frame = tk.Frame(date_time_main_frame)
date_time_L = tk.Label(date_time_frame, text="Date & Time: ")
date_time_L.pack(anchor="w", side=tk.LEFT)
date_time_B = tk.Button(date_time_frame, text="", command=date_time_F)
date_time_B.pack(anchor="w", side=tk.LEFT)
date_time_frame.pack(side=tk.TOP, anchor="w")
date_time_main_frame.pack(side=tk.TOP, anchor="w")

weather_description_main_frame = tk.Frame(report_data_frame)
weather_description_frame = tk.Frame(weather_description_main_frame)
weather_description_L = tk.Label(weather_description_frame, text="Weather: ")
weather_description_L.pack(anchor="w", side=tk.LEFT)
weather_description_B = tk.Button(weather_description_frame, text="", command=weather_description_F)
weather_description_B.pack(anchor="w", side=tk.LEFT)
weather_description_frame.pack(side=tk.TOP, anchor="w")
desc_note1_L = tk.Label(weather_description_frame)
desc_note1_L.pack(anchor="w", side=tk.TOP)
weather_description_main_frame.pack(side=tk.TOP, anchor="w")

temp_main_frame = tk.Frame(report_data_frame)
temp_frame = tk.Frame(temp_main_frame)
temp_L = tk.Label(temp_frame, text="Temperature: ")
temp_L.pack(anchor="w", side=tk.LEFT)
temp_B = tk.Button(temp_frame, text="", command=temp_F)
temp_B.pack(anchor="w", side=tk.LEFT)
temp_frame.pack(side=tk.TOP, anchor="w")
temp_main_frame.pack(side=tk.TOP, anchor="w")

humidity_main_frame = tk.Frame(report_data_frame)
humidity_frame = tk.Frame(humidity_main_frame)
humidity_L = tk.Label(humidity_frame, text="Humidity: ")
humidity_L.pack(anchor="w", side=tk.LEFT)
humidity_B = tk.Button(humidity_frame, text="", command=humidity_F)
humidity_B.pack(anchor="w", side=tk.LEFT)
humidity_frame.pack(side=tk.TOP, anchor="w")
humidity_main_frame.pack(side=tk.TOP, anchor="w")

wind_speed_main_frame = tk.Frame(report_data_frame)
wind_speed_frame = tk.Frame(wind_speed_main_frame)
wind_speed_L = tk.Label(wind_speed_frame, text="Wind Speed: ")
wind_speed_L.pack(anchor="w", side=tk.LEFT)
wind_speed_B = tk.Button(wind_speed_frame, text="", command=wind_speed_F)
wind_speed_B.pack(anchor="w", side=tk.LEFT)
wind_speed_frame.pack(side=tk.TOP, anchor="w")
wind_speed_main_frame.pack(side=tk.TOP, anchor="w")

#Frames which appear upon clicking for description button
desc_note_frame = tk.Frame(report_data_frame)
desc_note_L = tk.Label(desc_note_frame, text="Note: Click on information to bring or collapse description", font=("Calibri", 12, "bold"))
desc_note_L.pack(anchor="w", side=tk.TOP)
seperator2_frame = tk.Frame(desc_note_frame, height=3, bd=1, relief=tk.SUNKEN)
seperator2_frame.pack(fill='x')
creatorreport_L = tk.Label(desc_note_frame, text="Creator: Kewal Shah\nContact: work.kewalshah@gmail.com", font=("Calibri", 8, "bold"))
creatorreport_L.pack(side=tk.BOTTOM)
desc_note_frame.pack(side=tk.BOTTOM, anchor="w", pady=5)

date_time_desc_frame = tk.Frame(date_time_main_frame, highlightbackground="black", highlightthickness=1)
date_time1_L = tk.Label(date_time_desc_frame, text="The displayed data was recorded on -")
date_time1_L.pack(side=tk.TOP, anchor="w")
date_time2_L = tk.Label(date_time_desc_frame, text="")
date_time2_L.pack(side=tk.TOP, anchor="w", padx=10)
date_time3_L = tk.Label(date_time_desc_frame, text="")
date_time3_L.pack(side=tk.TOP, anchor="w", padx=10)

weather_description_desc_frame = tk.Frame(weather_description_main_frame, highlightbackground="black", highlightthickness=1, bg="dark grey")
weather_description1_L = tk.Label(weather_description_desc_frame, text="")
weather_description1_L.pack(side=tk.BOTTOM, pady=2)
weather_description2_L = tk.Label(weather_description_desc_frame, bg="dark grey")
weather_description2_L.pack(side=tk.TOP, pady=2)

temp_desc_frame = tk.Frame(temp_main_frame, highlightbackground="black", highlightthickness=1)
temp1_L = tk.Label(temp_desc_frame, text="")
temp1_L.pack(side=tk.TOP, pady=2)
temp2_L = tk.Label(temp_desc_frame, text="")
temp2_L.pack(side=tk.TOP)
temp_canvas = None

humidity_desc_frame = tk.Frame(humidity_main_frame, highlightbackground="black", highlightthickness=1)
humidity1_L = tk.Label(humidity_desc_frame, text="")
humidity1_L.pack(side=tk.TOP, pady=2)
humidity2_L = tk.Label(humidity_desc_frame, text="")
humidity2_L.pack(side=tk.TOP)
humidity_canvas = None

wind_speed_desc_frame = tk.Frame(wind_speed_main_frame, highlightbackground="black", highlightthickness=1)
wind_speed1_L = tk.Label(wind_speed_desc_frame, text="")
wind_speed1_L.pack(side=tk.TOP, pady=2)
wind_speed2_L = tk.Label(wind_speed_desc_frame, text="")
wind_speed2_L.pack(side=tk.TOP)
wind_speed_canvas = None

root.mainloop()