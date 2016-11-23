# onChambaMusicPlayer

##Simple music player for a 3 GPIO button raspberry pi

Run me on a raspberry pi/zero with 3 buttons connected on GPIO. 
At start I will load an m3u playlist and shuffle it.

Buttons provide -NEXT,PREVIOUS and Shuffle ALL/Current Artist- support

Needed packages:
	Music library created with beets. http://beets.io
	VLC and VLC python wrapper 

Special configuration:

Beets needs the play plugin enabled and configured like this:

````
play:
  command: python /home/no3z/onChambaMusicPlayer/beet_query.py
  use_folders: yes
  raw: yes
  warning_threshold: no
```

Change directory paths where applicable.
