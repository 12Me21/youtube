from os import listdir,path,chdir
import sys

home=path.dirname(path.abspath(__file__))
chdir(home)

name=sys.argv[1]

files=dict()
for file in listdir("songs"):
	files[file[0:11]] = file

with open("playlists/"+name+".txt",'r') as list:
	with open("playlists/"+name+".xspf",'w') as playlist:
		playlist.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		playlist.write('<playlist version="1" xmlns="http://xspf.org/ns/0/"><trackList>\n')
		for line in list:
			if line[0]!="#":
				id=line.rstrip()
				if id in files:
					playlist.write("<track><location>../songs/"+files[id]+"</location>\n")
					playlist.write("<image>file://"+home+"/thumbnails/"+id+".jpg</image></track>\n")
		playlist.write("</trackList></playlist>\n")
