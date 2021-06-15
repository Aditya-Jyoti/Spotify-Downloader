import requests
from urllib.parse import urlencode
from urllib.request import urlopen
import re
import json
from base64 import b64encode
from exceptions import AccessTokenExpired

with open('MY_SECRETS.json', 'r') as f:
    load_file = json.load(f)
    spotify_key = load_file['SPOTIFY_KEY']
    spotify_client_id = load_file['spotify_client_id']
    spotify_client_secret = load_file['spotify_client_secret']


def get_playlists(spotify_url):
    headers = {
        'Authorization': f'Bearer {spotify_key}'
    }

    playlist_id = spotify_url.split('/')[-1].split('?')[0]
    r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers)

    if r.json() == {'error': {'status': 401, 'message': 'The access token expired'}}:
        raise AccessTokenExpired('The Spotify Access Token Expired')
    else:
        returned_tracks = {}

        playlist_name = r.json()['name']

        for track in r.json()['tracks']['items']:
            song_name = track['track']['name']
            artists = []

            for artist in track['track']['artists']:
                artists.append(artist['name'])
            artist_name = ' '.join(artists)

            query_string = urlencode({'search_query': artist_name + ' ' + track['track']['name']})
            htm_content = urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())

            returned_tracks.update({f'{song_name}': f'http://www.youtube.com/watch?v={search_results[0]}'})

        return playlist_name, returned_tracks

def get_access_token():
    headers = {
        'Authorization': f'Basic {b64encode(f"{spotify_client_id}:{spotify_client_secret}".encode()).decode()}',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    r= requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    token = r.json()['access_token']

    updated_dict = {
        "spotify_client_id": f"{spotify_client_id}",
        "spotify_client_secret": f"{spotify_client_secret}",
        "SPOTIFY_KEY": token
    }

    with open('MY_SECRETS.json', 'w') as f:
        json.dump(updated_dict, f)