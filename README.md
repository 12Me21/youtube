this is a tool for creating archives of your youtube music (not to be confused with Youtube Music™) playlists, using youtube-dl.  
it will get a list of videos in a playlist, and download any that aren't already saved.  
files are downloaded in the highest quality audio format, and it writes metadata + downloads thumbnails  
creates a .xspf playlist file  

Dependencies:

make sure youtube_dl is in the python include path, somehow  
...I just created a symlink named `youtube_dl` in this directory to `.../youtube-dl/youtube_dl/`

Downloading a playlist:

- make sure the playlist is public or unlisted
- create a file named `playlists/<name>.txt`
- put the playlist id (JUST the id, not a url) on the first line of this file
- run `./main.py <name>`

Files:

- audio files will be downloaded to `songs/<video-id>.<extension>` (this is shared between playlists to reduce disk usage)
- thumbnails are downloaded to `thumbnails/<video-id>.jpg` (also shared)
- playlist files are saved as `playlist/<playlist-name>.xspf`

if a download fails, it will create `songs/<video-id>.fail`, so it won't check that video again. (delete `songs/*.fail` to force it to recheck)  
if you want to skip downloading certain videos (if they're too large or something) you can create a file named `songs/<video-id>.skip` or whatever


