from SpotifyDownloader.YoutubeDownloader import downloader
import argparse


parser = argparse.ArgumentParser(description='Download a Spotify Playlist')
parser.add_argument('-u','--URL', help='URL to the spotify playlist', required=True)
parser.add_argument('-p','--PATH', help='Location to download playlist', required=True)
args = vars(parser.parse_args())

if __name__ == '__main__':
    try:
        downloader(args['URL'], args['PATH'])
    except FileExistsError:
        print("""
The Location for download already has a file with similar name as the file trying to be created by the downloader
Try the following to fix this issue:
    1. Traverse to the location that you provided and if you see a folder named similar to that of the playlist
       that you are trying to download, delete that folder and run the program again
    2. Re-Run the program using the same location/path as provided in the earlier run

If this does not fix the issue or any new issues occur, create a new issue in GitHub or feel free to contact me
        """)
