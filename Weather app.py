# Import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = os.getenv("API_key")
    if not API_key:
        messagebox.showerror("Error", "API Key is missing.")
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    elif res.status_code != 200:
        messagebox.showerror("Error", "Unable to fetch data from OpenWeatherMap")
        return None

    # Parse the response JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Get the icon URL and return all weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

# Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from the URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.config(image=icon)
    icon_label.image = icon

    # Update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

# Set up the main application window
root = ttk.Window(themename="morph")
root.title('Weather app')
root.geometry('400x400')

# Entry widget for entering the city name
city_entry = ttk.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Button widget for searching for the weather information
search_button = ttk.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label widget for showing the city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Label widget for showing weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget for showing the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# Label widget for showing the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
