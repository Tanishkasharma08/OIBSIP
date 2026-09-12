"""
Basic Weather App — Advanced Tier
OASIS INFOBYTE — Python Programming Internship (Task 4)

Features:
- GUI window with city input field, "Get Weather" button, and results panel
- Displays current temperature, humidity, condition, and wind speed
- Weather icon fetched from OpenWeatherMap and shown in the GUI
- Hourly forecast panel (next 6 hours)
- Daily forecast panel (next 5 days)
- Celsius / Fahrenheit unit toggle
- Automatic location detection using the user's IP address (ipinfo.io) — bonus
- All error messages shown inside the GUI, not the terminal

SETUP REQUIRED:
1. Register for a free API key at https://openweathermap.org/api
2. Paste your key into the API_KEY variable below.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from io import BytesIO

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ---------------------------------------------------------------------------
# Configuration — paste your free OpenWeatherMap API key here
# ---------------------------------------------------------------------------
API_KEY = "795d0d22cf67b728e9f884e11eab217b"

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"
IP_LOCATION_URL = "https://ipinfo.io/json"


# ---------------------------------------------------------------------------
# API helper functions
# ---------------------------------------------------------------------------
def fetch_current_weather(city, units="metric"):
    """Fetch current weather data for a given city. Raises exceptions on failure."""
    params = {"q": city, "appid": API_KEY, "units": units}
    response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=8)
    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found. Please check the spelling.")
    if response.status_code == 401:
        raise ValueError("Invalid API key. Please check your OpenWeatherMap API key.")
    response.raise_for_status()
    return response.json()


def fetch_forecast(city, units="metric"):
    """Fetch the 5-day / 3-hour forecast data for a given city."""
    params = {"q": city, "appid": API_KEY, "units": units}
    response = requests.get(FORECAST_URL, params=params, timeout=8)
    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found. Please check the spelling.")
    response.raise_for_status()
    return response.json()


def fetch_city_from_ip():
    """Attempt to auto-detect the user's city using their IP address (free tier)."""
    try:
        response = requests.get(IP_LOCATION_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("city", "")
    except requests.RequestException:
        return ""


def fetch_icon_image(icon_code):
    """Download a weather icon and return a PhotoImage, or None if unavailable."""
    if not PIL_AVAILABLE:
        return None
    try:
        response = requests.get(ICON_URL.format(icon=icon_code), timeout=5)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return ImageTk.PhotoImage(image)
    except Exception:
        return None


def group_forecast_by_day(forecast_list):
    """
    Group the 3-hourly forecast entries by calendar day, returning a list of
    (date_str, representative_entry) tuples for the next 5 days.
    """
    days = {}
    for entry in forecast_list:
        date_str = entry["dt_txt"].split(" ")[0]
        # Prefer the midday (12:00) reading as representative of that day
        if date_str not in days or "12:00:00" in entry["dt_txt"]:
            days[date_str] = entry
    return list(days.items())[:5]


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Weather App — Advanced")
        self.root.geometry("560x680")
        self.root.configure(bg="#eaf2f8")
        self.units = "metric"  # metric = Celsius, imperial = Fahrenheit
        self.icon_refs = []     # keep references so images aren't garbage-collected

        self._build_widgets()

    def _build_widgets(self):
        tk.Label(
            self.root, text="🌤️ Weather App", font=("Helvetica", 20, "bold"),
            bg="#eaf2f8", fg="#2c3e50"
        ).pack(pady=(20, 10))

        # --- Search bar ---
        search_frame = tk.Frame(self.root, bg="#eaf2f8")
        search_frame.pack(pady=5)

        self.city_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=25)
        self.city_entry.grid(row=0, column=0, padx=5)
        self.city_entry.bind("<Return>", lambda e: self.on_get_weather())

        tk.Button(
            search_frame, text="Get Weather", font=("Helvetica", 11, "bold"),
            bg="#2980b9", fg="white", relief="flat", padx=8,
            command=self.on_get_weather
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            search_frame, text="📍 Use My Location", font=("Helvetica", 10),
            bg="#7f8c8d", fg="white", relief="flat", padx=6,
            command=self.on_use_location
        ).grid(row=0, column=2, padx=5)

        # --- Unit toggle ---
        self.unit_var = tk.StringVar(value="Celsius")
        unit_frame = tk.Frame(self.root, bg="#eaf2f8")
        unit_frame.pack(pady=5)
        tk.Radiobutton(unit_frame, text="Celsius (°C)", variable=self.unit_var, value="Celsius",
                        bg="#eaf2f8", command=self.on_unit_change).pack(side="left", padx=5)
        tk.Radiobutton(unit_frame, text="Fahrenheit (°F)", variable=self.unit_var, value="Fahrenheit",
                        bg="#eaf2f8", command=self.on_unit_change).pack(side="left", padx=5)

        # --- Current weather panel ---
        self.current_frame = tk.Frame(self.root, bg="white", relief="groove", bd=1)
        self.current_frame.pack(pady=15, padx=20, fill="x")

        self.icon_label = tk.Label(self.current_frame, bg="white")
        self.icon_label.pack(side="left", padx=10, pady=10)

        info_frame = tk.Frame(self.current_frame, bg="white")
        info_frame.pack(side="left", padx=10, pady=10)

        self.city_label = tk.Label(info_frame, text="—", font=("Helvetica", 14, "bold"), bg="white")
        self.city_label.pack(anchor="w")
        self.temp_label = tk.Label(info_frame, text="", font=("Helvetica", 22, "bold"), bg="white", fg="#2980b9")
        self.temp_label.pack(anchor="w")
        self.desc_label = tk.Label(info_frame, text="", font=("Helvetica", 11), bg="white")
        self.desc_label.pack(anchor="w")
        self.details_label = tk.Label(info_frame, text="", font=("Helvetica", 10), bg="white", fg="#7f8c8d")
        self.details_label.pack(anchor="w")

        # --- Hourly forecast ---
        tk.Label(self.root, text="Next 6 Hours", font=("Helvetica", 12, "bold"), bg="#eaf2f8").pack(pady=(10, 0))
        self.hourly_frame = tk.Frame(self.root, bg="#eaf2f8")
        self.hourly_frame.pack(pady=5)

        # --- Daily forecast ---
        tk.Label(self.root, text="Next 5 Days", font=("Helvetica", 12, "bold"), bg="#eaf2f8").pack(pady=(10, 0))
        self.daily_frame = tk.Frame(self.root, bg="#eaf2f8")
        self.daily_frame.pack(pady=5)

        # --- Error display area (inside GUI, not terminal) ---
        self.error_label = tk.Label(
            self.root, text="", font=("Helvetica", 10), bg="#eaf2f8", fg="#e74c3c", wraplength=500
        )
        self.error_label.pack(pady=10)

        self.last_city = None

    # ------------------------------------------------------------------
    def show_error(self, message):
        self.error_label.config(text=f"⚠️ {message}")

    def clear_error(self):
        self.error_label.config(text="")

    def on_unit_change(self):
        self.units = "metric" if self.unit_var.get() == "Celsius" else "imperial"
        if self.last_city:
            self._load_weather(self.last_city)

    def on_use_location(self):
        self.clear_error()
        city = fetch_city_from_ip()
        if not city:
            self.show_error("Could not auto-detect your location. Please enter a city manually.")
            return
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self._load_weather(city)

    def on_get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.show_error("Please enter a city name.")
            return
        self._load_weather(city)

    def _load_weather(self, city):
        self.clear_error()
        try:
            current = fetch_current_weather(city, self.units)
            forecast = fetch_forecast(city, self.units)
        except ValueError as e:
            self.show_error(str(e))
            return
        except requests.exceptions.Timeout:
            self.show_error("Network timeout. Please check your internet connection and try again.")
            return
        except requests.exceptions.RequestException as e:
            self.show_error(f"Network error: {e}")
            return

        self.last_city = city
        self._display_current(current)
        self._display_hourly(forecast["list"][:2])   # 2 entries × 3h = next 6 hours
        self._display_daily(group_forecast_by_day(forecast["list"]))

    def _unit_symbol(self):
        return "°C" if self.units == "metric" else "°F"

    def _display_current(self, data):
        unit = self._unit_symbol()
        self.city_label.config(text=f"{data['name']}, {data['sys']['country']}")
        self.temp_label.config(text=f"{data['main']['temp']:.1f}{unit}")
        self.desc_label.config(text=data["weather"][0]["description"].title())
        self.details_label.config(
            text=f"Humidity: {data['main']['humidity']}%   Wind: {data['wind']['speed']} m/s"
        )

        icon_code = data["weather"][0]["icon"]
        icon_img = fetch_icon_image(icon_code)
        if icon_img:
            self.icon_refs.append(icon_img)
            self.icon_label.config(image=icon_img)
        else:
            self.icon_label.config(image="", text="🌡️", font=("Helvetica", 30))

    def _display_hourly(self, entries):
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()

        unit = self._unit_symbol()
        for entry in entries:
            time_str = entry["dt_txt"].split(" ")[1][:5]
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["main"]

            card = tk.Frame(self.hourly_frame, bg="white", relief="groove", bd=1, padx=10, pady=8)
            card.pack(side="left", padx=5)
            tk.Label(card, text=time_str, font=("Helvetica", 10, "bold"), bg="white").pack()
            tk.Label(card, text=f"{temp:.0f}{unit}", font=("Helvetica", 12), bg="white").pack()
            tk.Label(card, text=desc, font=("Helvetica", 9), bg="white", fg="#7f8c8d").pack()

    def _display_daily(self, day_entries):
        for widget in self.daily_frame.winfo_children():
            widget.destroy()

        unit = self._unit_symbol()
        for date_str, entry in day_entries:
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["main"]

            card = tk.Frame(self.daily_frame, bg="white", relief="groove", bd=1, padx=8, pady=6)
            card.pack(side="left", padx=4)
            tk.Label(card, text=date_str[5:], font=("Helvetica", 9, "bold"), bg="white").pack()
            tk.Label(card, text=f"{temp:.0f}{unit}", font=("Helvetica", 11), bg="white").pack()
            tk.Label(card, text=desc, font=("Helvetica", 8), bg="white", fg="#7f8c8d").pack()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        print("⚠️  Please set your OpenWeatherMap API key in the API_KEY variable before running.")

    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()