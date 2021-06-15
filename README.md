## About 


This is a CLI (Command Line Interface) tool which downloads a spotify playlist,
meaning it downloads the MP3 version of the provided spotify playlist

Feel free to make pull requests

## Know Limitations and Issues


1. Take a very long time to actually download the playlist
2. Works only on my local machine since path and secret keys are hard coded
3. Raises `HTTP 404` error often (in process of fixing it)


## Installation Process


Run `$pip install -r requirements.txt` in your command line

## Usage


1. Clone the repository `$`
2. Traverse to the folder where the repository is cloned/ downloaded
3. Run `$py main.py -u URL-TO-PLAYLIST` in your command line
4. the `-u` parameter takes in the url to your spotify playlist
