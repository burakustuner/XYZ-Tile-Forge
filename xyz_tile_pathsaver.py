"""
/***************************************************************************
                                XYZ Tile Path Saver
 Saves the paths of generated XYZ tiles to a text file for easy access and reference.

 The XYZ Tile Path Saver script is designed to enumerate all the file paths
 within a specified directory that contains generated XYZ tiles, and save these
 paths to a text file. This utility aids in the management, documentation, and
 subsequent processing of tile datasets by providing a straightforward method
 to access the paths of individual tiles.

 The script navigates through the directory structure of the output directory
 specified in the configuration, listing every file path. It then writes these
 paths to a specified output file, preserving the logical organization of the
 tiles as represented by their file system paths.

                              -------------------
        date                 : 2024-02-27
        email                : burakustuner@gmail.com
        github               : github.com/burakustuner
 ***************************************************************************/

/***************************************************************************
 *                                                                        *
 * This script is shared in the spirit of open collaboration and         *
 * improvement. You are encouraged to use, modify, and distribute it      *
 * under the generous terms of the GNU General Public License (GPL)       *
 * version 3 or later. The GPL stands as a guarantee of freedom for       *
 * software, ensuring the rights to use, share, and modify this program   *
 * are preserved. For the full terms, see the GPL on the Free Software    *
 * Foundation's website.                                                  *
 *
 * Feel free to contact me for questions, suggestions, or discussions     *
 * about this project. I'm open to new ideas, collaborations, and helping *
 * others in any way possible.                                            *
 *                                                                        *
 ***************************************************************************/

Usage:
    - Configure the script by specifying the path to the output directory
      containing the XYZ tiles and the desired output file path for saving the tile paths.
    - Run the script in a Python environment. It will traverse the specified
      directory, list all the XYZ tile paths, and save them to the designated output file.

Parameters:
    config (dict): Configuration parameters for the path saving process.
        - scan_path: Path to the directory where XYZ tiles are stored.
Notes:
    - This script simplifies the task of documenting and accessing the file paths of
      large tile datasets.
    - Ensure the specified output directory exists to avoid any file writing errors.
"""

import os

import os

def xyz_tile_pathsaver(config):
    scan_path = config['scan_path']
    output_file_path = os.path.join(scan_path, 'tile_paths.txt')
    all_paths = []  # Dosya yollarını tutacak liste

    with open(output_file_path, 'w') as output_file:
        for root, dirs, files in os.walk(scan_path):
            relative_root = os.path.relpath(root, scan_path)  # root'un scan_path'e göre göreli yolu
            for file in files:
                if file.lower().endswith(('.jpg', '.png')):
                    # Dosya yolunu göreli olarak ekleyin ve dosya .jpeg, .jpg veya .png ile bitiyorsa
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