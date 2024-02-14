"""
/***************************************************************************
                                XYZ Tiler
 Generates XYZ tiles from a specified raster dataset using QGIS's Python API.

 The XYZ Tiler script automates the creation of map tiles in the XYZ format
 from a given raster layer, leveraging the 'qgis:tilesxyzdirectory' algorithm
 from the QGIS processing framework. This functionality allows for the efficient
 generation of tiles, suitable for use in web mapping applications
 or as a base map in various GIS projects.

 The tiling process converts a raster dataset into a series of map tiles
 at specified zoom levels, facilitating dynamic map rendering and scaling
 across different resolutions.

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
    - Ensure QGIS and necessary libraries are installed and configured.
    - Customize the script's configuration section with your raster path,
      output directory, and tile generation parameters.
    - Execute the script in a Python environment that has access to QGIS's libraries.

Functionality:
    The XYZ Tiler function (xyz_tiler) generates XYZ tiles based on the provided
    configuration using the 'qgis:tilesxyzdirectory' algorithm. This algorithm
    automates the process of tile generation for web mapping applications, exporting
    tiles for a range of zoom levels specified in the configuration.

Parameters:
    config (dict): Configuration parameters for the tile generation process.
        - qgis_main_path: Path to the QGIS installation directory.
        - xyz_raster_path: Path to the input raster file.
        - xyz_output_path: Path to the directory where tiles will be saved.
        - xyz_zoom_min: Minimum zoom level for tile generation.
        - xyz_zoom_max: Maximum zoom level for tile generation.
        - xyz_tile_format: Format of the generated tiles (0 for PNG, 1 for JPG).
        - xyz_dpi: DPI for the generated tiles.
        - xyz_background_color: Background color for the tiles in hex format.
        - xyz_quality: Quality of the generated tiles (relevant for JPG format).
        - xyz_metatilesize: Size of the meta-tile in tiles (improves performance).
        - xyz_tile_width: Width of each tile in pixels.
        - xyz_tile_height: Height of each tile in pixels.
        - xyz_tms_convention: Whether to use TMS tile naming convention.

Notes:
    - The script requires QGIS to be installed and properly configured on the system.
    - Adjust the script parameters based on your project's requirements.
    - The script's performance depends on the size of the raster dataset and the system's specifications.
"""

# Import necessary libraries from QGIS Python API
from qgis.core import QgsApplication, QgsProcessingFeedback, QgsRasterLayer
from qgis.analysis import QgsNativeAlgorithms

import sys
import os

def get_qgis_path(base_path, sub_path):
    # Attempt to use the qgis-ltr directory first
    qgis_ltr_path = os.path.join(base_path, "apps", "qgis-ltr", sub_path)
    if os.path.exists(qgis_ltr_path):
        return qgis_ltr_path
    # Fallback to the qgis directory if qgis-ltr does not exist
    qgis_path = os.path.join(base_path, "apps", "qgis", sub_path)
    if os.path.exists(qgis_path):
        return qgis_path
    # Raise an error if neither path exists
    raise FileNotFoundError(f"Neither qgis-ltr nor qgis directory found in {base_path}")


def xyz_tiler(config):
    # The QGIS Python library is accessed by adding the QGIS Python path to sys.path.
    qgis_path = config['qgis_main_path']+"apps/Python39"
    if qgis_path not in sys.path:
        sys.path.append(qgis_path)

    qgis_python_path = get_qgis_path(config['qgis_main_path'], "python")
    if qgis_python_path not in sys.path:
        sys.path.append(qgis_python_path)

    qgis_plugins_path = get_qgis_path(config['qgis_main_path'], "python/plugins")
    if qgis_plugins_path not in sys.path:
        sys.path.append(qgis_plugins_path)
    
    qgis_packages_path =  os.path.join(config['qgis_main_path'], "apps", "Python39", "lib", "site-packages")
    if qgis_packages_path not in sys.path:
        sys.path.append(qgis_packages_path)


    # Set environment variables for other QGIS and PyQt5 components
        
    # Dynamically setting the QT_QPA_PLATFORM_PLUGIN_PATH
    qt_plugin_path = os.path.join(config['qgis_main_path'], "apps", "qt5", "plugins")
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path

   # Dynamically adding to the PATH environment variable
    qgis_bin_path = get_qgis_path(config['qgis_main_path'], "bin")  # Adjust get_qgis_path if necessary to handle this case
    qt_bin_path = os.path.join(config['qgis_main_path'], "apps", "qt5", "bin")
    os.environ['PATH'] += ";" + qgis_bin_path + ";" + qt_bin_path

    # Dynamically setting the PYTHONHOME_PATH
    python_home_path = os.path.join(config['qgis_main_path'], "apps", "Python39")
    os.environ['PYTHONHOME'] = python_home_path

    #Dynamically settting the PYTHONPPATH_PATH
    python_path = os.path.join(config['qgis_main_path'], "apps", "Python39", "lib","site-packages")
    os.environ['PYTHONPATH'] = python_path


    from qgis.core import (
        QgsApplication,
        QgsProject,    
        QgsProcessingFeedback, 
        QgsRasterLayer,
        QgsCoordinateTransform,
        QgsCoordinateReferenceSystem
    )
    from qgis.analysis import QgsNativeAlgorithms

    # Starting the QGIS application
    qgis_prefix_path = get_qgis_path(config['qgis_main_path'])
    QgsApplication.setPrefixPath(qgis_prefix_path, True)

    qgs = QgsApplication([], False) # QGIS is started without a GUI when set to False. If true, it opens a GUI.
    qgs.initQgis()
    
    # Loads the Processing framework.
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Load the raster layer from provided path and check its validity
    raster_file = config['xyz_raster_path'] # Raster file path.
    raster_layer = QgsRasterLayer(raster_file, "raster")

    if raster_layer.isValid() ==False:
        print("Raster error...")
        exit() # If the layer cannot be loaded, the script is terminated.

    if not raster_layer.isValid():
        print("Layer failed to load!")
    else:
        # Converts the current coordinate reference system of the raster layer to the target CRS.
        source_crs = raster_layer.crs()
        target_crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
        transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
        # Converts the current extent of the layer.
        transformed_extent = transform.transformBoundingBox(raster_layer.extent())
        # Sets the EXTENT parameter using the converted extent.
        extent_str = "{},{},{},{}".format(transformed_extent.xMinimum(), transformed_extent.xMaximum(),transformed_extent.yMinimum(),  transformed_extent.yMaximum())

        print("extent in EPSG:4326= "+extent_str)

        # Prepare parameters for the XYZ tile generation    
        params = {
            'INPUT': raster_layer,
            'ZOOM_MIN': config['xyz_zoom_min'],
            'ZOOM_MAX': config['xyz_zoom_max'],
            'TILE_FORMAT': config['xyz_tile_format'],
            'DPI': config['xyz_dpi'],
            'BACKGROUND_COLOR':config['xyz_background_color'],
            'QUALITY':config['xyz_quality'],
            'METATILESIZE': config['xyz_metatilesize'],
            'TILE_WIDTH': config['xyz_tile_width'],
            'TILE_HEIGHT': config['xyz_tile_height'],
            'EXTENT':extent_str,
            #'EXTENT': '26.973651074,27.002737108,39.455455330,39.472725163 [EPSG:4326]',
            'TMS_CONVENTION':config['xyz_tms_convention'],
            'HTML_TITLE':config['xyz_html_title'],
            'HTML_ATTRIBUTION':config['xyz_html_attribution'],
            'HTML_OSM':config['xyz_html_osm'],
            'OUTPUT_DIRECTORY': config['xyz_output_path'],
            'OUTPUT_HTML': config['xyz_output_path']+'/preview.html'
        }
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(4326))
        QgsProject.instance().addMapLayer(raster_layer, True)
        # Starts process
        print("The XYZ Tile generation process is started. This may take some time, please be patient...")

        feedback = QgsProcessingFeedback()
        result = processing.run("qgis:tilesxyzdirectory", params, feedback=feedback)
        #print(result)
        print("XYZ Tile generation process completed. All layers have been successfully created :)")



    # Terminates the QGIS application.
    qgs.exitQgis()

if __name__ == "__main__":
    # Example configuration for testing
    config = {
        'qgis_main_path': "C:/Program Files/QGIS 3.34.3/",
        'xyz_raster_path': "path/to/your/raster/file.tif",
        'xyz_output_path': "path/to/output/directory",
        'xyz_zoom_min': 1,
        'xyz_zoom_max': 20,
        'xyz_tile_format': 0,  # 0 for PNG, 1 for JPG
        'xyz_dpi': 96,
        'xyz_background_color': '#00000000',
        'xyz_quality': 75,
        'xyz_metatilesize': 4,
        'xyz_tile_width': 256,
        'xyz_tile_height': 256,
        'xyz_tms_convention': False
    }
    xyz_tiler(config)
