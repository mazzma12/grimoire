# -*- coding: utf-8 -*-
# ---
# title: "Realizes Expedition"
# author: "Matthieu"
# date: "2022-12-25"
# categories: [news, map]
# image: "logo_carlina.png"
# format:
#   html:
#     code-fold: true
#     code-tools: true
# jupyter: python3
# toc: true
# execute:
#   echo: false
# ---

# %% [markdown]
#
# This is to present the trip of the boat Carlina part of the Realizes' exploration.
# This group of 6 young poeple aim at crossing the Atlantic on a boat while achieving scientific mission on the road.
#
# You may find details on their webpage : [here](https://linktr.ee/re_alizs?fbclid=PAAaadJsE1UKVq-_BnQXd2jrWstGOdGSEfgmXWzu6i-crtp7LXhLF0RbmlmGk)
#
# ## The trip
#
# Here is the itinerary
# %%
import geopandas as gpd


# %%
import re

import pandas as pd


# https://stackoverflow.com/questions/33997361
def dms2dd(s):
    # example: s = """0°51'56.29"S"""
    degrees, minutes, seconds, direction = re.split("[°'\"]+", s)
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction in ("S", "W"):
        dd *= -1
    return dd


def dm2dd(s):
    # example: s = """0°51'56.29"S"""
    decimal, direction = re.split("[°'\"]+", s)
    dd = float(decimal.replace(",", "."))
    if direction in ("S", "W"):
        dd *= -1
    return dd


# %%
gdf = gpd.read_file("waypoint_list.csv")
# %%
gdf = gdf.assign(
    name=gdf["Waypoint"].replace("WP", None).ffill(),
    lat=gdf["Phi"].map(dm2dd),
    lon=gdf["G"].map(dm2dd),
)
gdf = gdf.set_geometry(
    gpd.points_from_xy(
        gdf["lon"],
        gdf["lat"],
    )
)

# %%
locations_gdf = gdf.groupby("name", sort=False).first()
locations_gdf["line"] = gdf.groupby("name").geometry.apply(
    lambda x: [[xx.y, xx.x] for xx in x]
)


# %%
lines2 = []
for p1, p2 in zip(
    locations_gdf.geometry.iloc[
        :-1,
    ],
    locations_gdf.shift(-1).geometry,
):
    lines2.append([[p1.y, p1.x], [p2.y, p2.x]])

lines2.append(None)

locations_gdf["line2"] = lines2

# %%
import json

import geopandas
from ipywidgets import HTML
from ipyleaflet import (
    GeoData,
    LayersControl,
    Map,
    Polyline,
    basemaps,
    GeoJSON,
    Marker,
    FullScreenControl,
)

m = Map(
    center=(25.3, -10.0),
    zoom=2,
    # basemap=basemaps.Esri.WorldTopoMap
)

m.add_control(FullScreenControl())
geo_data = GeoData(
    geo_dataframe=locations_gdf,
    style={
        "color": "black",
        "fillColor": "#3366cc",
        "opacity": 0.05,
        "weight": 1.9,
        "dashArray": "2",
        "fillOpacity": 0.6,
    },
    hover_style={"fillColor": "red", "fillOpacity": 0.2},
    name="waipoints",
)

# m.add_layer(geo_data)
for idx, row in locations_gdf.iterrows():
    marker = Marker(location=(row.geometry.y, row.geometry.x), title=idx)

    message2 = HTML()
    message2.value = f"{idx}"
    marker.popup = message2
    m.add_layer(marker)

lines = Polyline(
    locations=locations_gdf["line2"].dropna().tolist(), color="green", fill=False
)
m.add_layer(lines)
m.add_control(LayersControl())
m
