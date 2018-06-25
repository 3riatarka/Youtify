#!/usr/bin/python3
# -*- encoding: utf8 -*-

import requests, os, sys, re, json, subprocess
from bs4 import BeautifulSoup

spotify_list = list()
youtube_links = list()
errors = list()
player = None

if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as inputf:
        for line in inputf:
            spotify_list.append(line.strip().strip())
else:
    print("You have to execute {} with one argument (spotify links)".format(sys.argv[0]))
    exit(1)

player = subprocess.Popen(['which', 'vlc'], stdout=subprocess.PIPE)
player = player.stdout.read()
player = player.strip().decode('utf-8')

for slink in spotify_list:
    req = requests.get(slink)
    if req.status_code == 200:
        spotify_regex = re.compile(r'Spotify.Entity = (.*);',re.MULTILINE)
        result = re.search(spotify_regex, req.text)
        info = json.loads(result.groups()[0])
        song_name = info['name']
        artist = ''
        for item in info['artists']:
            artist += item['name']+', '
        artist = artist[:-2]
        album = info['album']['name']

        qy_base_url = 'https://www.youtube.com/results?search_query='
        video_base_url = 'https://www.youtube.com'
        query = '{}+{}+{}'.format(song_name, artist, album)
        ytq = requests.get(qy_base_url+query)
        ytl = list()
        soup = BeautifulSoup(ytq.text, 'html.parser')

        for link in soup.find_all('a'):
            if 'href' in link.attrs and 'title' in link.attrs:
                if '/watch?v' in link.attrs['href']:
                    video = {'title':link.attrs['title'], 'link':video_base_url + link.attrs['href'] }
                    ytl.append(video)
        
        for video in ytl:
            if player:
                ans = ''
                while ans != 'y' and  ans != 'n':
                    ans = input('\nYT title: {}\n\t->Do you wish to preview it? [y/n] > '.format(video['title'], video['link']))
                    ans = ans.lower()

                if ans == 'y':
                    subprocess.Popen([player, video['link'], '>', '/dev/null'])
            else:
                print("\nYT title: {}".format(video['title']))

            ans = ''
            while ans != 'y' and ans != 'n':
                ans = input('\t -> Is it the correct video? [y/n] > ')
                ans = ans.lower()

            if ans == 'y':
                youtube_links.append(video['link'])
                break
        errors.append('{} ({}) not found in {}'.format(song_name, artist, video_base_url+query))           
    else:
        print("There was an error trying to get artist and song name from link ({}): {}".format(slink, ex))

error_file = open('error.log', 'w')
for error in errors:
    error_file.write(error)
error_file.close()

youtube_file = open('youtube_links.txt', 'w')
for link in youtube_links:
	youtube_file.write(link+'\n')
youtube_file.close()

print("\nDone")
