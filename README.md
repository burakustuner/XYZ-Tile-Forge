# XYZ Tile Forge

**Automates the process of generating, cleaning, and watermarking XYZ tiles**

---

**Date:** 2024-02-08  
**Email:** [burakustuner@gmail.com](mailto:burakustuner@gmail.com)  
**GitHub:** [github.com/burakustuner](https://github.com/burakustuner)

This script is shared with the spirit of open collaboration and improvement. You're encouraged to use, tweak, fold, spindle, or even mutilate it as you see fit under the generous terms of the GNU General Public License (GPL) version 3 or later. The GPL is a beacon of freedom for software, ensuring you always have the right to keep this program free, share your modifications, or even learn from its inner workings. For the full terms, check out the GPL on the [Free Software Foundation's website](https://www.fsf.org/).

Feel free to reach out if you have any questions, suggestions, or just want to chat about this project. I'm always open to discussing new ideas, collaboration, or helping out where I can.

## Description

The XYZ Tile Forge script is designed to automate the process of generating XYZ tiles from a given raster dataset, cleaning generated tiles based on file size criteria, and applying watermarks to the tiles. It integrates with QGIS, a free and open-source geographic information system, to utilize its spatial data processing capabilities.

The script is divided into three main functions:

- **xyz_tiler:** Generates XYZ tiles from a specified raster layer.
- **xyz_tile_cleaner:** Cleans the generated tiles by removing files below a specified size threshold.
- **xyz_tile_watermarker:** Adds a watermark to specified levels of tiles.

## Usage

Ensure QGIS is installed on your system as the script relies on QGIS's Python environment and processing algorithms. Modify the `main.py` script's parameters to match your project requirements and execute it from the command line or an IDE that supports Python.

## Preparation

- Install QGIS and ensure it is properly configured.
- Set Python's PATH environment variable to include QGIS's bin directory. Be carefull to declare proper qgis version.
  -PYTHONHOME = C:\Program Files\QGIS 3.28.15\apps\Python39
  -PYTHONPATH = C:\Program Files\QGIS 3.28.15\apps\Python39\lib\site-packages
- Adjust script parameters for dataset path, output directory, tile properties, and watermark specifications.
- Install necessary Python packages, if required (this should not be necessary).
- git config --global http.sslVerify false
- git config --global http.sslVerify true

## Execution

Run the script using a Python interpreter that has access to QGIS's libraries and processing framework.

The -i flag is for specifying the raster input file, and the -o flag is for specifying the output directory, -min flag is for specifying minimum zoom layer, -max flag is for specifiying maximum zoom layer.

```bash
  "C:/Program Files/QGIS 3.34.3/bin/python.exe" "E:/XYZ_Tiles/XYZ-Tile-Forge/main.py" -i "E:/XYZ_Tiles/originals/EPB/EB1/ayvalik" -o "E:/XYZ_Tiles/output" -min 7 -max 17

```
