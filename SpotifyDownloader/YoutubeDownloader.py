from SpotifyDownloader.SpotifyWebAPI import get_playlists, get_access_token
from pytube import YouTube
import os
from exceptions import AccessTokenExpired

def downloader(spotify_url):
    try:
        track = get_playlists(spotify_url)
    except AccessTokenExpired():
        get_access_token()
        track = get_playlists(spotify_url)

    path = f'G:\\youtube-mp3\\{track[0].replace(" ", "-")}'
    os.mkdir(path)

    for url in track[1].values():
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        video.download(path)
