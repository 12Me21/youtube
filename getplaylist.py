import sys
from youtube_dl import YoutubeDL
ydl = YoutubeDL()

def getplaylist(id):
	"Get a list of videos in a playlist"
	playlist = ydl.extract_info("https://youtube.com/playlist?list="+id, download=False, process=False)
	list = []
	for x in playlist['entries']:
		list+=[x]
	return list

for x in getplaylist(sys.argv[1]):
	print(x['id'])
