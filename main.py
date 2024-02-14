
"""
/***************************************************************************
                                 XYZ Tile Forge
 Automates the process of generating, cleaning, and watermarking XYZ tiles

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
"""

"""
 Description:
     The XYZ Tile Forge script is designed to automate the process of generating XYZ tiles from a given raster dataset,
     cleaning generated tiles based on file size criteria, and applying watermarks to the tiles.
     It integrates with QGIS, a free and open-source geographic information system, to utilize its spatial data processing capabilities.
   
     The script is divided into three main functions:
         - xyz_tiler: Generates XYZ tiles from a specified raster layer.
         - xyz_tile_cleaner: Cleans the generated tiles by removing files below a specified size threshold.
         - xyz_tile_watermarker: Adds a watermark to specified levels of tiles.

 Usage:
     Ensure QGIS is installed on your system as the script relies on QGIS's Python environment and processing algorithms.
     Modify the main.py script's parameters to match your project requirements and execute it from the command line or an IDE that supports Python.

 Preparation:
     - Install QGIS and ensure it is properly configured.
     - Adjust script parameters for dataset path, output directory, tile properties, and watermark specifications.
     - Install necessary Python packages, if required (this should not be necessary).

 Execution:
     Run the script using a Python interpreter that has access to QGIS's libraries and processing framework.
     The -i flag is for specifying the raster input file, and the -o flag is for specifying the output directory.
    "C:/Program Files/QGIS 3.34.3/bin/python.exe" "E:/XYZ_Tiles/scripts/main.py" -i "E:/XYZ_Tiles/ayvalik/AYVALIK_ORT.ecw" -o "E:/XYZ_Tiles/output"

 Post-Processing:
     Verify the generated tiles in the output directory, check for the application of watermarks, and ensure unwanted tiles were removed.
"""
# main.pya
import sys
import argparse
from datetime import datetime
# Add the path to QGIS Python libraries
sys.path.extend([
    'C:/Program Files/QGIS 3.34.3/apps/qgis/python',
    'C:/Program Files/QGIS 3.34.3/apps/Python39/lib/site-packages',
])
from xyz_tiler import xyz_tiler
from xyz_tile_cleaner import xyz_tile_cleaner
from xyz_tile_watermarker import xyz_tile_watermarker

def main():
    
    # Creating the argument parser
    parser = argparse.ArgumentParser(description='XYZ Tile Forge: Automates the process of generating, cleaning, and watermarking XYZ tiles.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input raster file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output directory for XYZ tiles.')

    # Parsing the arguments
    args = parser.parse_args()

    # Parameters for xyz_tiler
    tiler_config = {
        "qgis_main_path": "C:/Program Files/QGIS 3.34.3/",
        "xyz_raster_path": args.input,
        "xyz_output_path": args.output,
        #"xyz_raster_path": "E:/XYZ_Tiles/ayvalik/AYVALIK_ORT.ecw",
        #"xyz_output_path": "E:/XYZ_Tiles/output",
        "xyz_zoom_min": 1,
        "xyz_zoom_max": 20,
        "xyz_tile_format": 0,  # 0 for PNG, 1 for JPG
        "xyz_dpi": 96,
        "xyz_background_color": '#FFFFFF00',
        "xyz_quality": 74,
        "xyz_metatilesize": 4,
        "xyz_tile_width": 256,
        "xyz_tile_height": 256,
        "xyz_tms_convention": False,
        "xyz_html_title": '',
        "xyz_html_attribution": '',
        "xyz_html_osm": False
    }

    # Parameters for xyz_tile_cleaner
    cleaner_config = {
        "clear_zoom_min": 1,
        "clear_zoom_max": 25,
        "clear_size_min": 5169,  # 1711 for jpeg_19, 5169 for png_19
        "clear_path": tiler_config['xyz_output_path']
        #"clear_path": "E:/XYZ_Tiles/output"
    }

    # Parameters for xyz_tile_watermarker
    watermarker_config = {
        "watermark_directory":tiler_config['xyz_output_path'],
        #"watermark_directory": "E:/XYZ_Tiles/output",
        "watermark_text": "@2024",
        "watermark_layer_levels": [14,15,17],
        "watermark_font_path": "arial.ttf",
        "watermark_font_size": 10,
        "watermark_text_color": (255, 255, 255, 10),
        "watermark_margin_left": 10,
        "watermark_margin_bottom": 10,
        "watermark_frequency": 5
    }

    # Call the functions
    start_time = datetime.now()
    xyz_tiler(tiler_config)
    xyz_tile_cleaner(cleaner_config)
    xyz_tile_watermarker(watermarker_config)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"All processes have been successfully completed in '{int(hours)} hour {int(minutes)} min {int(seconds)} sec'.")

if __name__ == "__main__":
    main()
