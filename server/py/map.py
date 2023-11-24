#!/usr/bin/env python3

import folium
import sqlite3
import pandas as pd
from folium.plugins import HeatMap

conn = sqlite3.connect("/usr/local/share/ping_results.db")

df = pd.read_sql_query("SELECT latitude, longitude, rssi FROM results", conn)

df_folium = pd.DataFrame(
    {
        "Lat": df["latitude"],
        "Long": df["longitude"],
        "RSSI": df["rssi"].str.rstrip(" dBm").astype(float),
    }
)
df_folium["weight"] = df_folium["RSSI"].astype(float) / df_folium["RSSI"].max()

df_folium = df_folium.dropna(subset=["Lat", "Long", "weight"])

m = folium.Map(location=[32.907112, -96.950261], zoom_start=15, control_scale=True)

values = df_folium[["Lat", "Long", "weight"]]

for lat, long, rssi in zip(df_folium["Lat"], df_folium["Long"], df_folium["RSSI"]):
    if rssi <= -95:
        color = "red"
    elif rssi <= -85:
        color = "orange"
    elif rssi <= -75:
        color = "lightgreen"
    elif rssi <= -65:
        color = "green"
    else:
        color = "darkgreen"

    folium.Marker(
        location=[lat, long],
        popup=f"RSSI: {rssi}",
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(m)

m.save("test.html")
