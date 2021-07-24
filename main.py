#!/usr/bin/env python
from __future__ import unicode_literals
from os import listdir,path,chdir,chmod
from sys import argv,stdout
import re
import urllib

home=path.dirname(path.abspath(__file__))
chdir(home)

ydl = None

class Video(object):
	_lastDownload = None
	_files = {}
	file = None
	thumbnail = None
	info = None
	id = None
	def __init__(self, id):
		self.id = id
		self._files[id] = self
	def __new__(self, id):
		if id in self._files:
			return self._files[id]
		return super(Video, self).__new__(self, id)
	def __str__(self):
		return "{"+self.id+": "+(self.file or "NONE")+","+(self.thumbnail or "NONE")+"}"
	def __repr__(self):
		return self.__str__()
	def downloadVideo(self):
		initYTDL()
		from youtube_dl.utils import DownloadError
		filename = None
		try:
			ydl.download(["https://youtu.be/"+self.id])
			filename = self._lastDownload['filepath']
			chmod(filename, 0o444)
		except DownloadError:
			filename = "songs/"+self.id+".fail"
			with open(filename, "w") as f:
				f.write(repr(self.info))
		self.file = filename
	def downloadThumbnail(self):
		filename = "thumbnails/"+id+".jpg"
		urllib.urlretrieve('https://i.ytimg.com/vi/'+id+'/mqdefault.jpg', filename)
		chmod(filename, 0o444)
		self.thumbnail = filename
	def get(self):
		if not self.file:
			self.downloadVideo()
		if not self.thumbnail:
			self.downloadThumbnail()
	@staticmethod
	def getExisting():
		songname_re = re.compile(r"^([\w_-]{11})\.\w+$")
		for filename in listdir("songs"):
			match = songname_re.match(filename)
			if match:
				Video(match.group(1)).file = "songs/"+filename
		for filename in listdir("thumbnails"):
			match = songname_re.match(filename)
			if match:
				Video(match.group(1)).thumbnail = filename

Video.getExisting()

ydl = None

def makePlaylist(name):
	"Generate playlist file"
	with open("playlists/"+name+".txt",'r') as list,\
	     open("playlists/"+name+".xspf",'w') as playlist:
		playlist.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		playlist.write('<playlist version="1" xmlns="http://xspf.org/ns/0/"><trackList>\n')
		for line in list:
			id=line.rstrip()
			if id[0]=="#": continue
			info = Video(id)
			if info.file:
				playlist.write("<track><location>../"+info.file+"</location>\n")
				playlist.write("<image>file://"+home+"/thumbnails/"+id+".jpg</image></track>\n")
		playlist.write('</trackList></playlist>\n')

def writePlaylist(name, items):
	with open("playlists/"+name+".txt",'w') as list:
		list.write(playlistId+"\n")
		for item in items:
			list.write(item['id']+"\n")

def readPlaylist(name):
	items = []
	with open("playlists/"+name+".txt",'r') as list:
		first = True
		for line in list:
			id=line.rstrip()
			if id[0]=="#": continue
			if not first:
				items += [{'id':id}]
			first = False
	return items

def getPlaylist(id):
	"Get a list of videos in a playlist"
	initYTDL()
	playlist = ydl.extract_info("https://youtube.com/playlist?list="+id, download=False, process=False)
	list = []
	for x in playlist['entries']:
		list+=[x]
	return list

def initYTDL():
	global ydl
	if ydl: return
	print("waiting for ytdl to start...")
	from youtube_dl import YoutubeDL
	from youtube_dl.postprocessor.common import PostProcessor
	ydl = YoutubeDL({
		'format': 'bestaudio/best',
		'outtmpl': 'songs/%(id)s.%(ext)s',
		'continue_dl': True,
		'addmetadata': True,
		'postprocessors': [{
			'key': 'FFmpegMetadata',
		},{
			'key': 'FFmpegExtractAudio',
		}]
	})
	class TestPP(PostProcessor):
		def run(self, inf):
			Video._lastDownload = inf #hack
			return [], inf
	ydl.add_post_processor(TestPP())

name = argv[1]
playlistId = None
with open("playlists/"+name+".txt",'r') as list:
	for line in list:
		playlistId = line.rstrip()
		break # just read the first line lol

if len(argv) < 3:
	print("getting playlist...")
	items = getPlaylist(playlistId);
	writePlaylist(name, items)

items = readPlaylist(name);

print "playlist: "+name
print "id: "+playlistId

failed = 0
skipped = 0
got = 0
missing = 0
for item in items:
	id = item['id']
	info = Video(id)
	info.info = item
	file = info.file
	if file:
		if file.endswith(".fail"):
			failed+=1
			print "failed: "+file
		elif file.endswith(".skip"): skipped+=1
		else: got+=1
	else:
		missing+=1
print "  Total: "+str(len(items))
print "   Have: "+str(got)
if missing: print "Missing: "+str(missing)
if failed: print " Failed: "+str(failed)
if skipped: print "Skipped: "+str(skipped)
print

print("downloading new videos... ("+str(missing)+")")
for item in items:
	id = item['id']
	info = Video(id)
	info.get()

print("generating playlist file...")
makePlaylist(name)
print("done...")

