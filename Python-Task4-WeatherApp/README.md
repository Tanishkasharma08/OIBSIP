# Basic Weather App — Advanced (Python Programming Track, Task 4)

## 📌 Objective
A GUI weather application that fetches and displays real-time weather data,
hourly and daily forecasts, and supports automatic location detection —
built using the OpenWeatherMap API.

## 🛠️ Tech Stack
- Python 3
- `requests` — API calls
- `tkinter` — GUI
- `Pillow (PIL)` — displaying weather icons
- OpenWeatherMap API (free tier)

## ✅ Features
- GUI with a city input field, **Get Weather** button, and results panel
- Displays current temperature, humidity, weather description, and wind speed
- **Weather icons** fetched live from OpenWeatherMap and shown in the GUI
- **Hourly forecast** — next 6 hours
- **Daily forecast** — next 5 days
- **Celsius / Fahrenheit toggle** — instantly re-renders in the selected unit
- **Auto location detection** ("Use My Location" button) via the free
  `ipinfo.io` IP-lookup API — bonus feature
- All errors (city not found, network timeout, invalid API key) are shown
  **inside the GUI**, never as terminal print statements

## 🔑 Setup (Required Before Running)
1. Register for a **free API key** at [openweathermap.org](https://openweathermap.org/api)
   (free tier allows 60 calls/minute — more than enough for this app).
2. Open `weather_app.py` and replace the placeholder:
   ```python
   API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
   ```
   with your actual key.

## ▶️ How to Run
```bash
pip install requests pillow
python weather_app.py
```

## 🗂️ Project Structure
```
OIBSIP/Python-Task4-WeatherApp/
├── weather_app.py     # Main application
├── README.md           # This file
└── screenshots/         # App screenshots 
```

## 🧪 How It Works
1. Enter a city name and click **Get Weather** (or press Enter), or click
   **Use My Location** to auto-detect your city.
2. Current conditions, an icon, and a summary appear at the top.
3. Scroll down to see the **hourly forecast** (next 6 hours) and
   **daily forecast** (next 5 days).
4. Toggle between **Celsius** and **Fahrenheit** at any time — the display
   updates instantly using the last searched city.

## ⚠️ Notes
- An active internet connection is required.
- If you see "Invalid API key", note that newly created OpenWeatherMap keys
  can take a few minutes to a couple of hours to activate.

## 👤 Author
Submitted as part of the **Oasis Infobyte Summer Internship Program (SIP)**
— Python Programming Track.
