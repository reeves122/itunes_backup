import csv
import logging
import os
import plistlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logging.getLogger()
FIELD_LIST = ['Track ID', 'Persistent ID', 'Artist', 'Album', 'Name', 'Track Number', 'Genre',
              'Loved', 'Disliked', 'Rating', 'Play Count', 'Play Date',
              'Track Type', 'Apple Music']
XML_PATH = '/iTunes/iTunes Music Library.xml'
EXPORT_PATH = '/export'


def load_library(xml_path: str) -> dict:
    """
    Load and parse the iTunes XML Library file

    :param xml_path:    Path to iTunes XML file
    :return:            Dict of parsed library
    """
    logging.info(f'Loading iTunes XML File: "{xml_path}"')
    with open(xml_path, 'rb') as handle:
        return plistlib.load(handle)


def build_playlist_file_name(playlist_item: dict, export_path: str) -> str:
    """
    Build the file name used to export a playlist

    :param playlist_item:   Playlist item dict from iTunes library
    :param export_path:     Base path to export playlist
    :return:                String of path and filename
    """
    file_name = f"{playlist_item.get('Name', 'empty')} " \
                f"({playlist_item.get('Playlist Persistent ID', 'none')}).csv"

    # Remove special characters that will mess up the path
    file_name = file_name.replace('\\', '-')
    file_name = file_name.replace('/', '-')

    return os.path.join(export_path, file_name)


def initialize_csv(csv_file_name: str) -> csv.writer:
    """
    Create an open an output CSV file with header written

    :param csv_file_name:   Path and name of CSV file to create
    :return:                csvwriter object
    """
    file_handle = open(csv_file_name, 'wt')
    writer = csv.writer(file_handle, delimiter=',')
    writer.writerow(FIELD_LIST)
    return writer


def get_playlist_track_values(playlist_track: dict, itunes_library: dict) -> list:
    """
    Look up the properties for a playlist track. A playlist track only includes a Track ID so
    we must use that to fetch the track properties from the Tracks section of the library.

    :param playlist_track:      Playlist track dict containing a Track ID
    :param itunes_library:      iTunes library Dict
    :return:                    List of property values, based on the FIELD_LIST variable
    """
    track_id = str(playlist_track.get('Track ID'))
    track = itunes_library['Tracks'].get(track_id, {})

    return [track.get(field) for field in FIELD_LIST]


def main():
    """
    Main entry point

    :return:    None
    """
    logging.info('Starting itunes_backup.py')
    library = load_library(XML_PATH)

    for playlist in library.get('Playlists', []):

        file_name = build_playlist_file_name(playlist, '/export')
        logging.info(f'Exporting playlist tracks to file: "{file_name}"')

        writer = initialize_csv(file_name)

        for item in playlist.get('Playlist Items', []):
            writer.writerow(get_playlist_track_values(item, library))

    logging.info('Done exporting playlists')


if __name__ == '__main__':
    main()
