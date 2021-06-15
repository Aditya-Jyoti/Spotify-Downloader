from SpotifyDownloader.YoutubeDownloader import downloader
import argparse

parser = argparse.ArgumentParser(description='Download a Spotify Playlist')
parser.add_argument('-u','--URL', help='URL to the spotify playlist', required=True)
args = vars(parser.parse_args())

if __name__ == '__main__':
    downloader(args['URL'])
