# -*- coding: utf-8 -*-
import sys
import os
import csv
import re
from gmusicapi import Mobileclient
import unicodecsv
from config import *

# Fix windows console encoding. `chcp 65001` to unicode and `chcp 950` to big5
import codecs
#codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

# log
logfile = codecs.open("foobar_gmusic.log", encoding='utf-8', mode='w', buffering=1)

# log to both the console and log file
def log(message, proceed = True):
    if not proceed:
        return
    print message.encode(sys.stdout.encoding, errors='replace')
    logfile.write(message)
    logfile.write(os.linesep)

def decode(s):
    return s\
        .replace('\\n','\n')\
        .replace('\\t','\t')\
        .replace(r'\'',"'")\
        .replace(r'\"','"')

def s_in_s(string1,string2,start=u''):
    if not string1 or not string2:
        return False
    s1 = re.compile('[\W_]+', re.UNICODE).sub(u'',string1.lower())
    s2 = re.compile('[\W_]+', re.UNICODE).sub(u'',string2.lower())
    return re.search(start+s1,s2) or re.search(start+s2,s1)

# Read csv
log("##### Reading CSV #####")

f = open('foobar.csv', 'r')  
rows = []
for row in unicodecsv.DictReader(f):  
    rows.append(row)

f.close()

log("##### Login Google Music #####")

# Login into Google Music
api = Mobileclient()
api.login(gmusic_username, gmusic_password)

log("##### Fetching Library #####")

library = api.get_all_songs()

# Search all songs
songs = []
missing = []

log("##### Matching Songs #####")

for row in rows:
	found = False
	for song in library:
		if decode(row['title']) == song['title'] and \
			decode(row['artist']) == song['artist'] and \
			s_in_s(decode(row['album']), song['album']) and\
			int(row['tracknum']) == song['trackNumber']:
			log("Song " + decode(row['title']) + " Found. ID: " + song['id'])
			songs.append(song)
			found = True
			break

	if found == False:
		missing.append(row)
	
print "##### {} of {} Songs Found. #####".format(len(songs), len(rows))

log("### Missing Songs ###")

for row in missing:
	log(decode(row['title']) + " could not be found.")

log("### Fetching Playlists ###")
playlists = api.get_all_user_playlist_contents()
playlist = [p for p in playlists if p['name'] == gmusic_playlist_name]

song_ids = [s['id'] for s in songs]

if len(playlist) == 0: # Playlist not found, create a new one.
	playlist_id = api.create_playlist(u'foobar2000')
else:
	playlist_id = playlist[0]['id']
	# Prevent duplicated songs in existing playlist
	for track in playlist[0]['tracks']:
		if track['trackId'] in song_ids:
			song_ids.remove(track['trackId'])

log("Importing to Playlist ID: " + playlist_id)
api.add_songs_to_playlist(playlist_id, song_ids)

log("### Import Completed ###")

logfile.close()
api.logout()