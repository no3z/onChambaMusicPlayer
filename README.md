# onChambaMusicPlayer
Simple music player for a 3 button raspberry pi

Simple project to run on a raspberry pi with 3 buttons connected on GPIO. At start it will load an m3u playlist and shuffle it.
Buttons provide -NEXT,PREVIOUS and Shuffle ALL/Current Artist- support

Needed packages:
	Music library created with beets. 
	VLC and VLC python wrapper

Also, beets needs the play plugin enabled and configured like this:

play:
  command: python /home/no3z/onChambaMusicPlayer/beet_query.py
  use_folders: yes
  raw: yes
  warning_threshold: no

