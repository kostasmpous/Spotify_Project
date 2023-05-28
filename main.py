import json
import os
import base64
import matplotlib.pyplot as plt


from requests import post
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_key = '8ad48719173f42fd89a84c3b22b2f897'
client_secret = '53c733a1087348b4a6d57f5fcdf4db4f'
load_dotenv()

# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=client_key, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_items(playlist_URI)["items"]]
data = {
    'uri': [],
}
tracks_uri = []
tracks_name = []
art_uri = []
art_info = []
art_name = []
art_pop = []
art_genre = []
alb = []
pop_track = []

for track in sp.playlist_items(playlist_URI)["items"]:
    # URI
    tracks_uri.append(track["track"]["uri"])
    # Track name
    tracks_name.append(track["track"]["name"])

    # Main Artist

    artist_uri = track["track"]["artists"][0]["uri"]
    art_uri.append(artist_uri)
    artist_info = sp.artist(artist_uri)
    art_info.append(artist_info)

    # Name, popularity, genre
    art_name.append(track["track"]["artists"][0]["name"])
    art_pop.append(artist_info["popularity"])
    art_genre.append(artist_info["genres"])

    # Album
    album = track["track"]["album"]["name"]
    alb.append(album)
    # Popularity of the track
    track_pop = track["track"]["popularity"]
    pop_track.append(track_pop)

data = {
    "track name": tracks_name,
    "artist name": art_name,
    "popularity": art_pop,
    "genre": art_genre,
    "album name": alb,

}
plt.close("all")
df = pd.DataFrame(data=data)
df1 = df[df["genre"].str.len()>0]
genres={}
for x in df1["genre"]:
    for j in x:
        if j in genres.keys():
            genres[j] = genres[j]+1
        else:
            genres[j] = 1

genres1 = list(genres.keys())
numbers = genres.values()


plt.bar(range(len(genres)),numbers,tick_label=genres1)
plt.xticks(rotation='vertical')
plt.show()
