
################################
##        ORGANIZER EXT       ##
##                            ##
##  Version: 1.0.             ##
##  Create Name: WillhemM.    ##
##  Date Create: 07-02-24.    ##
##                            ##
################################

import os
import json
import shutil
import exifread
from datetime import datetime

# consult the application's configuration json.
def file_configure():
    try:
        with open('config.json') as file:
            read = json.load(file)
        return read
    except OSError as err:
        print("Error: (0)".format(err))
    return

def get_creation_or_modification_date(file_path):
    try:
        # If it fails, get the modification date
        modification_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(modification_time).year
    except Exception as e:
        print(f"Error getting creation date for {file_path}: {e}")
        try:
            # Try to obtain the creation date
            creation_time = os.path.getctime(file_path)
            return datetime.fromtimestamp(creation_time).year
        except Exception as e:
            print(f"Error getting modification date for {file_path}: {e}")
    return None

def organize_media_files(source_folder):
    images_folder = os.path.join(source_folder, 'Images')
    videos_folder = os.path.join(source_folder, 'Videos')

    unrecognized_formats = set()

    # Create destination folders if they do not exist
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(videos_folder, exist_ok=True)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if file.lower().endswith(('.aae', '.jpg', '.heic', '.png', '.webp')):
                year = get_creation_or_modification_date(file_path)
                if year is not None:
                    destination_folder = os.path.join(images_folder, str(year))
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(destination_folder, file))
                else:
                    unrecognized_formats.add(file)

            elif file.lower().endswith(('.mp4', '.mov')):
                year = get_creation_or_modification_date(file_path)
                if year is not None:
                    destination_folder = os.path.join(videos_folder, str(year))
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(destination_folder, file))
                else:
                    unrecognized_formats.add(file)

            else:
                unrecognized_formats.add(file)

    # Delete empty folders
    for folder in [source_folder]:
        for root, dirs, files in os.walk(folder, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):  # Check if the folder is empty
                    os.rmdir(dir_path)

    if unrecognized_formats:
        print("Unrecognized formats:")
        for format in unrecognized_formats:
            print(format)

# main function
if __name__ == '__main__':
    path_to_process = file_configure()[0]['path']
    organize_media_files(path_to_process)
    print("Process completed")