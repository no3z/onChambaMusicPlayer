#!/usr/bin/python

import vlc
import RPi.GPIO as GPIO
import time
import sys
import os

GPIO.setmode(GPIO.BCM)

NEXT=13
PREV=12
CHANGE=6

GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CHANGE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_mode="ALL"
artist = "Unknown"

in_query_m3u="/media/sda/Playlists/query.m3u"
out_query_m3u="/media/sda/Playlists/query_shuffle.m3u"

PLAYLIST="/media/sda/Playlists/all_shuffle.m3u"
IN_PLAYLIST="/media/sda/Playlists/all.m3u"

def shuffle_m3u(input, output):
	os.system("python /home/no3z/onChambaMusicPlayer/shuffle.py -i %s -o %s" % (input, output))

def cb_next(channel):
        print "Next"
	lp.next()

def cb_prev(channel):
	lp.previous()
	print "Previous"

def cb_switch_all_album(channel):
        global artist
        global current_mode
	lp.stop()
	if artist != "Unknown" and current_mode=="ALL":
        	print "Creating", artist, "playlist."
                os.system("sudo -u no3z beet play %s" % artist.encode('UTF-8'))
                shuffle_m3u(in_query_m3u,out_query_m3u)
                ml= vlc.MediaList()
                ml.add_media(out_query_m3u)
                lp.set_media_list(ml)
                lp.play()
                current_mode="ARTIST"
	elif current_mode=="ARTIST":
                print "Switch to all"
                shuffle_m3u(IN_PLAYLIST, PLAYLIST)
                ml= vlc.MediaList()
                ml.add_media(PLAYLIST)
                lp.set_media_list(ml)
                lp.play()
                current_mode="ALL"

def mediachanged(event, player):
	global artist
	media = player.get_media()
	media.parse()
	artist = media.get_meta(vlc.Meta.Artist) or "Unknown"
	title = media.get_meta(vlc.Meta.Title) or "Unknown"
	album = media.get_meta(vlc.Meta.Album) or "Unknown"
	print artist, title, album
	

GPIO.add_event_detect(NEXT, GPIO.FALLING, callback=cb_next, bouncetime=300)
GPIO.add_event_detect(PREV, GPIO.FALLING, callback=cb_prev, bouncetime=300)
GPIO.add_event_detect(CHANGE, GPIO.FALLING, callback=cb_switch_all_album, bouncetime=300)

i = vlc.Instance('-A', 'alsa,none' '--alsa-audio-device default')
p = vlc.MediaPlayer()
lp = vlc.MediaListPlayer()
lp.set_media_player(p)

mp_ev = p.event_manager()
mp_ev.event_attach(vlc.EventType.MediaPlayerMediaChanged, mediachanged, p)

ml= vlc.MediaList()

shuffle_m3u(IN_PLAYLIST, PLAYLIST)

ml.add_media(PLAYLIST)
lp.set_media_list(ml)
lp.play()

try:
   while True:
      time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit


