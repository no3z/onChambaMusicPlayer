#!/bin/python

import sys

with open('/media/sda/Playlists/query.m3u','w') as file:
	file.write("\n".join(sys.argv))


