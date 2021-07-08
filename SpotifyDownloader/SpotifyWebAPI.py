import requests
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import json
from base64 import b64encode


def get_playlists(spotify_url):
    with open('MY_SECRETS.json', 'r') as f:
        spotify_key = json.load(f)['SPOTIFY_KEY']

    playlist_id = spotify_url.split('/')[-1].split('?')[0]
    r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers={'Authorization': f'Bearer {spotify_key}'})

    if r.status_code == 400 or r.status_code == 401:
        raise TypeError('Invalid Spotify Token')

    returned_tracks = {}

    playlist_name = r.json()['name']

    r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers={'Authorization': f'Bearer {spotify_key}'})
    data = r.json()

    tracks = data['items']
    while data['next']:
        r = requests.get(data['next'], headers={'Authorization': f'Bearer {spotify_key}'})
        data = r.json()
        tracks = tracks + data['items']

    for track in tracks:
        song_name = track['track']['name']
        artists = []

        for artist in track['track']['artists']:
            artists.append(artist['name'])
        artist_name = ' '.join(artists)

        try:
            query_string = urlencode({'search_query': artist_name + ' ' + song_name})
            htm_content = urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())

            returned_tracks.update({f'{song_name}': f'http://www.youtube.com/watch?v={search_results[0]}'})

        except HTTPError:
            print(f'Couldn\'t download "{song_name}", continuing')
            continue

    return playlist_name, returned_tracks


def get_access_token():
    with open('MY_SECRETS.json', 'r') as f:
        load_file = json.load(f)
        spotify_client_id = load_file['spotify_client_id']
        spotify_client_secret = load_file['spotify_client_secret']

    headers = {
        'Authorization': f'Basic {b64encode(f"{spotify_client_id}:{spotify_client_secret}".encode()).decode()}',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    r = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    token = r.json()['access_token']

    updated_dict = {
        "spotify_client_id": f"{spotify_client_id}",
        "spotify_client_secret": f"{spotify_client_secret}",
        "SPOTIFY_KEY": token
    }

    with open('MY_SECRETS.json', 'w') as f:
        json.dump(updated_dict, f)
