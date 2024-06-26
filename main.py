
"""
/***************************************************************************
                                 XYZ Tile Forge
 Automates the process of generating, cleaning, watermarking, and archiving
 XYZ tiles on Windows OS using QGIS and Python.

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
 *                                                                        *
 * Feel free to reach out if you have  any questions, suggestions, or just *
 * want to chat about this project. I'm always open to discussing new     *
 * ideas, collaboration, or helping out where I can.                     *
 *                                                                        *
 ***************************************************************************/

/***************************************************************************
 * Description:                                                            *
 *     The XYZ Tile Forge script is designed to automate the process of   *
 *     generating XYZ tiles from a given raster dataset, cleaning          *
 *     generated tiles based on file size criteria, applying watermarks    *
 *     to the tiles, and archiving the processed tiles for easy            *
 *     distribution and storage. It integrates with QGIS, a free and       *
 *     open-source geographic information system, to utilize spatial data  *
 *     processing capabilities. Additionally, it automatically detects the *
 *     extent of raster files given.                                       *
 *                                                                         *
 *     The script is divided into five main parts:                         *
 *         - xyz_tiler: Generates XYZ tiles from a specified raster layer. *
 *         - xyz_tile_cleaner: Cleans the generated tiles by removing      *
 *           files below a specified file size threshold.                  *
 *         - xyz_tile_watermarker: Adds watermark to specified levels of   *
 *           tiles.
 *         - xyz_tile_pathsaver: Saves the paths of processed tiles into a *
 *           text file for documentation and further processing.                                                  *
 *         - xyz_tile_archiver: Archives the processed tiles into a zip    *
 *           file for easy distribution and storage.                       *
 *                                                                         *
 * Usage:                                                                  *
 *     Ensure QGIS is installed on your system as the script requires QGIS *
 *     Python environment and processing algorithms. Modify the main.py    *
 *     script's parameters to match your project requirements and execute  *
 *     it from the command line, .bat file or an IDE that supports Python. *
 *                                                                         *
 * Preparation:                                                            *
 *     - Install QGIS and be sure it is properly configured.               *
 *     - Set Python's PATH environment variable to include QGIS's bin      *
 *       directory. Be careful to declare the proper QGIS version.         *
 *       - PYTHONHOME = C:\Program Files\QGIS 3.28.15\apps\Python39        *
 *       - PYTHONPATH = C:\Program Files\QGIS 3.28.15\apps\Python39\lib\   *
 *                       site-packages                                     *
 *     - Adjust script parameters for dataset path, output directory, tile *
 *       properties, and watermark details.                                *
 *     - Install necessary Python packages, if required (this should not   *
 *       be necessary with Qgis installed on Windows OS).                  *
 *                                                                         *
 * Execution:                                                              *
 *     - The `-i` flag is for specifying the raster input file.            *
 *     - The `-o` flag is for specifying the output directory where the    *
 *       XYZ tiles will be saved.                                          *
 *     - The `-min` flag is for specifying the minimum zoom layer for the  *
 *       XYZ tile generation.                                              *
 *     - The `-max` flag is for specifying the maximum zoom layer for the  *
 *       XYZ tile generation.                                              *
 *     - The `-zip` flag is an optional flag; when used, it enables        *
 *       archiving of the output directory into a zip file for easy        *
 *       distribution and storage.                                         *
 *     - The `-mark` flag is for specifying the watermark text to be       *
 *       applied to the tiles. This flag is optional.                      *
 *     - The `-plog` flag is for creating a txt file which contains XYZ    *
 *       tile paths. This flag is optional.                                *
 *                                                                         *
 *     For example, to generate tiles with a minimum zoom of 7 and a       *
 *     maximum zoom of 17, apply a watermark "2024", and zip the output    *
 *     directory, you can run:                                             *
 *                                                                         *
 *     "C:/Program Files/QGIS 3.34.3/bin/python.exe" "E:/XYZ_Tiles/        *
 *     XYZ-Tile-Forge/main.py" -i "E:/XYZ_Tiles/originals/EPB/EB1/ayvalik/ *
 *     ayvalik_ort.ecw" -o "E:/XYZ_Tiles/output" -min 7 -max 17 -zip -mark  *
 *     "2024"                                                              *
 *                                                                         *
 * Notes:                                                                  *
 *     Verify the generated tiles in the output directory, check for the   *
 *     application of watermarks, and ensure unwanted empty tiles were     *
 *     removed.                                                            *
 ***************************************************************************/

"""
# main.py

import argparse
from datetime import datetime
import logging
import os

from xyz_tiler import xyz_tiler
from xyz_tile_cleaner import xyz_tile_cleaner
from xyz_tile_watermarker import xyz_tile_watermarker
from xyz_tile_archiver import xyz_tile_archiver
from xyz_tile_pathsaver import xyz_tile_pathsaver

def main():
    
    # Creating the argument parser
    parser = argparse.ArgumentParser(description='XYZ Tile Forge: Automates the process of generating, cleaning, and watermarking XYZ tiles.')
    parser.add_argument('-i', '--input', required=False, help='Path to the input raster file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output directory for XYZ tiles.')
    parser.add_argument('-min', '--minlayer', required=False, help= 'Minimum zoom layer for XYZ tiles.')
    parser.add_argument('-max', '--maxlayer', required=False, help='Maximum zoom layer for XYZ tiles.')
    parser.add_argument('-clear', '--clear', required=False, help='Remove tiles below threshold.')
    parser.add_argument('-mark', '--watermark', required=False, help='Watermark text to be applied')
    parser.add_argument('-zip', '--zip', action='store_true', help='Enable archiving of the output directory into a zip file.')  # Sıkıştırma opsiyonu eklendi
    parser.add_argument('-plog', '--pathlog', action='store_true', help='Enable creating a pathway list of xyz tiles.')

    # Parsing the arguments
    args = parser.parse_args()



    # Parameters for xyz_tiler
    tiler_config = {
        "qgis_main_path": "C:/Program Files/QGIS 3.34.3/",
        "xyz_raster_path": args.input,
        "xyz_output_path": args.output,
        "xyz_zoom_min": args.minlayer,
        "xyz_zoom_max": args.maxlayer,
        #"xyz_raster_path": "E:/XYZ_Tiles/ayvalik/AYVALIK_ORT.ecw",
        #"xyz_output_path": "E:/XYZ_Tiles/output",
        #"xyz_zoom_min": 1,
        #"xyz_zoom_max": 17,
        "xyz_tile_format": 1,  # 0 for PNG, 1 for JPG
        "xyz_dpi": 96,
        "xyz_background_color": '#FFFFFF00',
        "xyz_quality": 95,
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
        "clear_size_min": args.clear,  # 1800 for jpeg 85, 5169 for png
        "clear_path": tiler_config['xyz_output_path']
        #"clear_path": "E:/XYZ_Tiles/output"
    }

    # Parameters for xyz_tile_watermarker
    watermarker_config = {
        "watermark_directory":tiler_config['xyz_output_path'],
        #"watermark_directory": "E:/XYZ_Tiles/output",
        "watermark_text": args.watermark,
        #"watermark_text": "@BOTAS 2024",
        "watermark_layer_levels": [14,15,18,19],
        "watermark_font_path": "arial.ttf",
        "watermark_font_size": 10, #10 for png
        "watermark_text_color": (255, 255, 255), # (255, 255, 255, 10), for png
        "watermark_margin_left": 5, #10 for png 
        "watermark_margin_bottom": 50, #10 for png
        "watermark_frequency": 6,
        "watermark_stroke_width":1, # Konturun kalınlığını ayarla
        "watermark_stroke_fill":(0,0,0)  # Konturun rengini belirle
    }

    pathsaver_config = {
        "scan_path":tiler_config['xyz_output_path'],
    }

    zipper_config = {
        "archive_path": tiler_config['xyz_output_path'],  # Directory to be zipped
        "zip_file_path": f"{tiler_config['xyz_output_path']}/{os.path.basename(tiler_config['xyz_output_path'])}.zip"  # Destination for the zip file

    }

    # Call the functions
    start_time = datetime.now()

    if args.input:
        xyz_tiler(tiler_config)
    else:
        print("No raster file specified. Proceeding without generating XYZ tiles. [-i  'E:/XYZ_Tiles/originals/EPB/EB1/MAGA DGBH/Maga.ecw']")
    if args.clear:
        xyz_tile_cleaner(cleaner_config)
    else:
        print("Cleainng process skipped. [-clear 1800] ")
    if args.watermark:
        xyz_tile_watermarker(watermarker_config)
    else:
        print("No watermark text specified. Proceeding without watermarking. [-mark 'example']")
    
    if args.pathlog:
        xyz_tile_pathsaver(pathsaver_config)
    else:
        print("Path log step is skipped as per command line option [-plog].")

    if args.zip:
        xyz_tile_archiver(zipper_config)
    else:
        # skip zip process
        print("Archiving (zipping) step is skipped as per the command line option [-zip].")

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"All processes have been successfully completed in '{int(hours)} hour {int(minutes)} min {int(seconds)} sec'.")
    
    # Setting up logging
    log_file = os.path.join(args.output, 'Forge_Log.txt')
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Log the parameters
    logging.info(f"Input file: {args.input}")
    logging.info(f"Output directory: {args.output}")
    logging.info(f"Minimum zoom layer: {args.minlayer}")
    logging.info(f"Maximum zoom layer: {args.maxlayer}")
    logging.info(f"All processes have been successfully completed in '{int(hours)} hour {int(minutes)} min {int(seconds)} sec'.")


if __name__ == "__main__":
    main()
