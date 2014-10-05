## fpl2gmusic

This tool imports foobar2000 playlist(fpl) into a Google Music Playlist.

I use foobar2000 autoplaylist(`%rating% GREATER 0`) along with this tool to sync my favorites(rating) with Google Music.

## Usage

* Edit `config.py`.

* Edit `sync.bat` specify the correct fpl path.

* Run `sync.bat` when you want to sync the playlist.

*Note the fpl filename could be changed when you change the playlist order, try place your target playlist at the first.*

## Notes

Basically this tool calls [fplreader](https://github.com/tetrisfrog/fplreader) to export foobar2000 playlist to csv 
and then try to match those metadata with your Google Music Library. I had my foobar2000 libaray and Google Music library 
synchronized so there's no problem.

This only fits my personal use, read the code before you try it.
