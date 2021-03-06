# vesper2-export

This script exports your notes from [Vesper](http://vesperapp.co) as a folder of text files.

It operates on a copy of your Vesper data files. You can get these using one of those “iPhone backup explorer” tools or by following [these command-line instructions](http://stackoverflow.com/a/13793043/371228). Vesper’s files are located in `/AppDomain-co.qbranch.vesper`.

## Instructions

1. Download the script by clicking the “Download ZIP” button to the right or by following [this link](https://github.com/bdesham/vesper2-export/archive/master.tar.gz).
2. Decompress the file you just downloaded.
3. Open a Terminal window and run a command like this:

        ~/Downloads/vesper2-export-master/vesper2-export.py \
            ~/Desktop/AppDomain-co.qbranch.vesper \
            ~/Desktop/vesper-files

    The first argument to the script is the folder with Vesper’s files in it. The second argument is the folder where the exported files should be written; this folder will be created if it doesn’t exist already. The script will print some progress as it goes.

## Export format

This script produces a folder full of text files, one per Vesper note. The name of each file comes from the first line of the note. The files are numbered so that they will appear in the same order in the Finder as in Vesper. Archived notes are put into an “Archive” folder and numbered separately.

Each text file contains the entire text of a note, including whatever part of the first line was used in the filename. If the note had tags, there will be a line at the end of the file like “Tags: App ideas, Travel plans”. The tags are presented in the same order here as they were in Vesper.

Images attached to your notes are given the same name as the note (so they’ll appear next to each other in the Finder) but have the appropriate extension for their file type, e.g. “.jpeg”.

## Compatibility

The script reads data from Vesper 2.x files. If you want to export data from Vesper 1.x, check out Brian Partridge’s [VesperExport](https://github.com/brianpartridge/VesperExport) script.

This is a Python script. It has been designed to work with Python 2.7, which comes with OS X 10.10 and 10.11; it probably won’t work with Python 3 without some tweaks.

## Version history

* Version 1.0 (October 8, 2015): first public release.

## Author

This script was created by [Benjamin Esham](https://esham.io).

This project is [hosted on GitHub](https://github.com/bdesham/vesper2-export). Please feel free to submit pull requests.

## License

Copyright © 2015 Benjamin D. Esham. This program is released under the ISC license, which you can find in the file LICENSE.md.
