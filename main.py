import tkinter as tk
from tkinter import ttk, messagebox
import random
import requests

# Simulate SDS011 sensor readings
def get_sds011_data():
    # Simulate PM2.5 and PM10 values
    pm25 = round(random.uniform(5, 50), 1)
    pm10 = round(random.uniform(10, 80), 1)
    return {"PM2.5": pm25, "PM10": pm10}

# Fetch regional air quality data (dummy API endpoint)
def get_regional_data(postcode):
    # Simulate API response
    return {"PM2.5": random.randint(10, 30), "PM10": random.randint(20, 50)}

# Compare data
def compare_data(sensor_data, regional_data):
    result = []
    for key in sensor_data:
        diff = sensor_data[key] - regional_data[key]
        result.append(f"{key}: {'Higher' if diff > 0 else 'Lower'} ({abs(diff):.1f} µg/m³)")
    return "\n".join(result)

# Main application class
class AirQualityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Air Quality Monitor")
        self.geometry("400x400")
        self.configure(bg="#f7f7f9")
        self.user_info = {}

        self.frames = {}
        for F in (WelcomeFrame, OnboardingFrame, DashboardFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeFrame)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

# Welcome screen
class WelcomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f7f7f9")
        ttk.Label(self, text="Welcome to the Air Quality App", font=("Helvetica", 16), background="#f7f7f9").pack(pady=40)
        ttk.Label(self, text="Monitor and compare air quality in your area!", font=("Helvetica", 10), background="#f7f7f9").pack(pady=10)
        ttk.Button(self, text="Get Started", command=lambda: parent.show_frame(OnboardingFrame)).pack(pady=20)

# Onboarding screen
class OnboardingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f7f7f9")

        ttk.Label(self, text="Tell us about yourself!", font=("Helvetica", 14), background="#f7f7f9").pack(pady=20)

        ttk.Label(self, text="Your Name:", background="#f7f7f9").pack(anchor="w", padx=20)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5, padx=20, fill="x")

        ttk.Label(self, text="Your Postcode:", background="#f7f7f9").pack(anchor="w", padx=20)
        self.postcode_entry = ttk.Entry(self)
        self.postcode_entry.pack(pady=5, padx=20, fill="x")

        ttk.Button(self, text="Submit", command=self.submit_details).pack(pady=20)

    def submit_details(self):
        name = self.name_entry.get().strip()
        postcode = self.postcode_entry.get().strip()

        if not name or not postcode:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.master.user_info = {"name": name, "postcode": postcode}
        self.master.show_frame(DashboardFrame)

# Dashboard screen
class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f7f7f9")

        self.label = ttk.Label(self, text="", font=("Helvetica", 14), background="#f7f7f9")
        self.label.pack(pady=20)

        self.sensor_data_label = ttk.Label(self, text="", font=("Helvetica", 12), background="#f7f7f9")
        self.sensor_data_label.pack(pady=10)

        self.compare_label = ttk.Label(self, text="", font=("Helvetica", 12), background="#f7f7f9")
        self.compare_label.pack(pady=10)

        ttk.Button(self, text="Refresh Data", command=self.update_data).pack(pady=20)

    def update_data(self):
        user_info = self.master.user_info
        name = user_info.get("name")
        postcode = user_info.get("postcode")

        sensor_data = get_sds011_data()
        regional_data = get_regional_data(postcode)
        comparison = compare_data(sensor_data, regional_data)

        self.label.config(text=f"Hello, {name}! Here is the air quality data for {postcode}:")
        self.sensor_data_label.config(text=f"Sensor Data:\nPM2.5: {sensor_data['PM2.5']} µg/m³\nPM10: {sensor_data['PM10']} µg/m³")
        self.compare_label.config(text=f"Comparison with regional data:\n{comparison}")

# Run the application
if __name__ == "__main__":
    app = AirQualityApp()
    app.mainloop()
