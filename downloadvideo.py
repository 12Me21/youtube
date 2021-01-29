import sys
from youtube_dl import YoutubeDL
ydl = YoutubeDL({
	'format': 'bestaudio/best',
	'outtmpl': '%(id)s.%(ext)s',
	'continue_dl': True,
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
	}]
})

def download(id):
	"Download a video"
	url = "https://youtu.be/"+id
	ydl.download([url])

for line in sys.stdin:
   if line[0]!="#":
      id=line.rstrip()
      download(id)
