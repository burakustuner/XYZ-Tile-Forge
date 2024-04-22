"""
/***************************************************************************
                                XYZ Tile Path Saver
 This script simplifies the task of documenting and accessing the file paths
 of large tile datasets.

 The XYZ Tile Path Saver script is designed to get all the file paths
 in a given directory that contains generated XYZ tiles, and save these
 paths to a text file. 

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
    - Configure the script by selecting the path to the output directory
      containing the XYZ tiles and the output file path for saving the tile paths.
    - Run the script in a Python environment. The script navigates through the
      directory structure of the output directory given in the configuration, 
      then writes all found paths to the output file.
      
Parameters:
    config (dict): Configuration parameters for the path saving process.
        - scan_path: Path to the directory where XYZ tiles stored.
Notes:
    - 
"""

import os

import os

def xyz_tile_pathsaver(config):
    scan_path = config['scan_path']
    output_file_path = os.path.join(scan_path, 'tile_paths.txt')
    all_paths = []  # Dosya yollarını tutacak liste

    with open(output_file_path, 'w') as output_file:
        for root, dirs, files in os.walk(scan_path):
            relative_root = os.path.relpath(root, scan_path)  # root'un scan_path'e göre relative yolu
            for file in files:
                if file.lower().endswith(('.jpg', '.png')):
                    # Dosya yolunu relative olarak ekle uzantısı ile birlikte (.jpeg, .jpg veya .png)
                    relative_file_path = os.path.join(relative_root, file) if relative_root != "." else file
                    all_paths.append(relative_file_path + '\n')

        # Tüm yolları bir kerede dosyaya yaz
        output_file.writelines(all_paths)

    print(f"Paths of XYZ tiles have been saved to {output_file_path}")


if __name__ == "__main__":
    # Example configuration for testing
    config = {
        "scan_path": "path/to/output/directory",
    }
    xyz_tile_pathsaver(config)