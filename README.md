# itunes_backup
Python script for backing up iTunes playlists as CSV files.
This script will load the iTunes XML file and export each playlist as a CSV file.
There will also be a `Library.csv` file containing all tracks in the library.

## Set iTunes to create XML file
The script requires the iTunes XML file, which is not created by iTunes by default.
1. Open iTunes preferences
2. Go to the Advanced tab
3. Click to enable the `Share iTunes Library XML with other applications` box


## Build Using Docker
First, build the docker image using `docker build -t itunes_backup .`
This only needs to be done once, or if the script is updated.


## Run Using Docker
The script expects two paths to exist:

  - `/iTunes` - Containing the iTunes XML file. Ex: `C:\Users\foo\Music\iTunes`
  - `/export` - The directory you would like to back up playlists

These paths should be set when running docker.
The below example will mount the local iTunes directory for a user names "foo" and playlists will be
exported to the user's Downloads directory in a new folder called itunes_backup

`docker run -v C:\Users\foo\Music\iTunes:/iTunes -v C:\Users\foo\Downloads\itunes_backup:/export itunes_backup`
