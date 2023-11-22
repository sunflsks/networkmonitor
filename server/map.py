#!/usr/bin/env python3

import folium
import sqlite3
import pandas as pd
from folium.plugins import HeatMap

conn = sqlite3.connect("demo/ping_results_sample.db")

df = pd.read_sql_query("SELECT latitude, longitude, rssi FROM results", conn)

df_folium = pd.DataFrame(
    {"Lat": df["latitude"], "Long": df["longitude"], "RSSI": df["rssi"]}
)
df_folium["weight"] = df_folium["RSSI"].astype(float) / df_folium["RSSI"].max()

m = folium.Map(location=[32.907112, -96.950261], zoom_start=15, control_scale=True)

values = df_folium[["Lat", "Long", "weight"]]
data = values.values.tolist()

hm = HeatMap(data, min_opacity=0.2, radius=15, blur=10, max_zoom=1)
m.add_child(hm)
m.save("test.html")
