"""
/***************************************************************************
                                XYZ Tile Cleaner
 Cleans generated XYZ tiles by removing files below a specified size threshold.

 The XYZ Tile Cleaner script is designed to optimize tile storage by deleting
 tiles that fall below a minimum file size. This is particularly useful for
 removing empty or nearly empty tiles that do not contribute meaningful data to
 the map. By specifying minimum file size and zoom level range, users can
 precisely target and remove unnecessary tiles, reducing storage requirements
 and potentially improving map loading times.

 The script iterates over directories corresponding to specified zoom levels,
 checking each tile's file size against the provided threshold. Tiles smaller
 than the threshold are deleted, preserving only those tiles that meet or
 exceed the specified size criteria.

                              -------------------
        date                 : 2024-02-08
        copyright            : (C) 2024 by burakustuner
        email                : burakustuner@gmail.com
        github               : github.com/burakustuner
 ***************************************************************************/

/***************************************************************************
 *                                                                        *
 * This script is shared with the spirit of open collaboration and        *
 * improvement. You're encouraged to use, tweak, fold, spindle, or even   *
 * mutilate it as you see fit under the generous terms of the GNU General *
 * Public License (GPL) version 3 or later. The GPL is a beacon of        *
 * freedom for software, ensuring you always have the right to keep this  *
 * program free, share your modifications, or even learn from its inner   *
 * workings. For the full terms, check out the GPL on the Free Software   *
 * Foundation's website.                                                  *

 * Feel free to reach out if you have any questions, suggestions, or just *
 * want to chat about this project. I'm always open to discussing new     *
 * ideas, collaboration, or helping out where I can.                      *
 *                                                                        *
 ***************************************************************************/

Usage:
    - Configure the script with the directory path of the generated XYZ tiles,
      the minimum file size for tiles to be retained, and the range of zoom
      levels to be cleaned.
    - Execute the script in a Python environment. It will automatically traverse
      the specified directory structure, removing any tiles that do not meet the
      size criteria.

Parameters:
    config (dict): Configuration parameters for the tile cleaning process.
        - clear_path: Path to the directory where XYZ tiles are stored.
        - clear_size_min: Minimum file size (in bytes) for tiles to be retained.
        - clear_zoom_min: Minimum zoom level at which cleaning should start.
        - clear_zoom_max: Maximum zoom level at which cleaning should end.

Notes:
    - The script aims to enhance tile storage efficiency by eliminating
      low-value tiles, potentially reducing overall storage needs and
      improving the performance of web mapping applications.
    - It is advisable to backup your tile data before running the cleaning
      process, especially if applying the script to a production dataset.
"""

import os

def xyz_tile_cleaner(config):
    clear_path = config['clear_path']
    clear_size_min = config['clear_size_min']
    clear_zoom_min = config['clear_zoom_min']
    clear_zoom_max = config['clear_zoom_max']
    
    # Function to delete tiles smaller than the specified size
    def delete_small_tiles(directory, size_threshold):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) < size_threshold:
                    os.remove(file_path)

    # Iterate over specified zoom levels and clean tiles
    for zoom_level in range(clear_zoom_min, clear_zoom_max + 1):
        zoom_level_path = os.path.join(clear_path, str(zoom_level))
        if os.path.exists(zoom_level_path):
            print(f"Cleaning tiles in zoom level {zoom_level}...")
            delete_small_tiles(zoom_level_path, clear_size_min)
        else:
            print(f"Zoom level {zoom_level} directory does not exist. Skipping...")

    print("Tile cleaning process completed.")

if __name__ == "__main__":
    # Example configuration for testing
    config = {
        'clear_path': "path/to/output/directory",
        'clear_size_min': 5169,  # Size threshold in bytes
        'clear_zoom_min': 1,
        'clear_zoom_max': 25
    }
    xyz_tile_cleaner(config)
