from SpotifyDownloader.SpotifyWebAPI import get_playlists, get_access_token
from pytube import YouTube
from urllib.error import HTTPError
import os


def downloader(spotify_url, location):
    try:
        track = get_playlists(spotify_url)
    except TypeError:
        get_access_token()
        track = get_playlists(spotify_url)

    path = f'{location}\\{track[0].replace(" ", "-")}'

    os.makedirs(path)

    dict_of_playlist = track[1]

    for url_name in dict_of_playlist:
        try:
            yt = YouTube(dict_of_playlist[url_name])
            video = yt.streams.filter(only_audio=True).first()
            video.download(path)

            print(f"Downloaded {url_name} at -> {path}")

        except HTTPError:
            print(f'Couldn\'t download "{url_name}", continuing')
            continue

