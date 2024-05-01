"""
/***************************************************************************
                                XYZ Tile Archiver
 Archives the generated XYZ tiles by zipping them into a single file.

 The XYZ Tile Archiver script is designed to compress the entire directory
 of generated XYZ tiles into a single zip archive. This helps with easy
 distribution, backup, and storage of tile datasets.

 The script uses Python's built-in zipfile module to create the archive,
 iterating over the files and directories in given tile output directory 
 and adding them to the zip file.

                              -------------------
        author               : burak üstüner
        date                 : 2024-02
        email                : burakustuner@gmail.com
        github               : github.com/burakustuner
 ***************************************************************************/

/***************************************************************************
 *                                                                        *
 * This script is shared with the spirit of open collaboration and        *
 * improvement. You're encouraged to use, tweak, fold, spindle, or even   *
 * mutilate it as you see fit under the generous terms of the GNU General *
 * Public License (GPL) version 3 or later. For the full terms, check out *
 * the GPL on the Free Software Foundation's website.                     *

 * Feel free to reach out if you have any questions, suggestions, or just *
 * want to chat about this project. I'm always open to discussing new     *
 * ideas, collaboration, or helping out where I can.                      *
 *                                                                        *
 ***************************************************************************/

Usage:
    - Configure the script with the path to the output directory containing
      the XYZ tiles and the destination path for the zip archive.
    - Execute the script in a Python environment. It will automatically compress
      the directory into a zip file with the directory structure.

Parameters:
    config (dict): Configuration parameters for the archiving process.
        - archive_path: Path to the directory where XYZ tiles are stored.
        - zip_file_path: Destination path for the created zip file.

Notes:
    - 
"""

import os
import zipfile

def xyz_tile_archiver(config):
    archive_path = config['archive_path']
    zip_file_path = config['zip_file_path']
    
    # Function to zip the directory
    def zip_directory(folder_path, zip_path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                # Ana klasördeki zip dosyalarını hariç tut
                if root == folder_path:
                    files = [f for f in files if not f.endswith('.zip')]

                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, archive_path))

    print(f"Archiving tiles from {archive_path} to {zip_file_path}...")
    zip_directory(archive_path, zip_file_path)
    print("Archiving process completed.")



if __name__ == "__main__":
    # Example configuration for testing
    config = {
        'archive_path': "path/to/output/directory",
        'zip_file_path': "path/to/destination/archive.zip"
    }
    xyz_tile_archiver(config)

