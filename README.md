# Youtify
Convert spotify links to youtube links. It has been tested on python3.5 only.

## Installation
Get the script with `git clone https://github.com/GDVG/Youtify`, and then install required modules with `sudo pip3 install -r requirements.txt`.

## How to use it
The script takes one argument (a list of spotify song web links). If you have VLC installed on your system, the script offers a preview of each youtube link to pick the right one. Otherwise, it only shows the video title.

Run it with `python3 youtify.py <spotify link list file>` or give it execution permission and run it with the `./` syntax.

The youtube links are written to 'youtube_links.txt' (overwritten at the end of each execution). This file could be supplied to [youtube-dl](https://github.com/rg3/youtube-dl) to automate downloading.

###### Module info
The modules needed to run it are:
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): needed for Youtube site scraping, to get the video links
* [Requests](http://docs.python-requests.org/en/master/): for web requests, to get information both from Spotify and Youtube websites
