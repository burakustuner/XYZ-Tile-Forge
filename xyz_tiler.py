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

import sys
import os
    # Determine if the qgis or qgis-ltr version installed on system.
def get_qgis_ltr(base_path, sub_path):
    # Attempt to use the qgis-ltr directory first
    paths = ["qgis-ltr", "qgis"]
    for path in paths:
        full_path = os.path.join(base_path, "apps", path, sub_path)
        if os.path.exists(full_path):
            return full_path
    raise FileNotFoundError(f"Neither qgis-ltr nor qgis directory found in {base_path}")


def add_to_sys_path(path):
    """Append the given path to sys.path if it's not already included."""
    if path not in sys.path:
        sys.path.append(path)
        print(path +" added to sys.path")
    else:
        print(path +" already in sys.path")

def configure_qgis_paths(qgis_main_path):
    """Configures paths related to QGIS to be included in Python's sys.path."""
    # Define the base path for QGIS Python packages
    paths = [
        os.path.join(qgis_main_path, "apps", "Python39"),  # Main QGIS Python path
        os.path.join(qgis_main_path, "apps", "Python39", "lib", "site-packages"),  # Site-packages path
        get_qgis_ltr(qgis_main_path, "python"),  # General QGIS Python path
        get_qgis_ltr(qgis_main_path, "python/plugins"),  # QGIS Python plugins path
    ]
    
    # Append paths to sys.path
    for path in paths:
        add_to_sys_path(path)

def set_environment_variable(key, value):
    """Set or update an environment variable and notify about the change."""
    if key in os.environ:
        print(f"{key} environment variable updated.")
    else:
        print(f"{key} environment variable set.")
    os.environ[key] = value

def configure_environment_variables(qgis_main_path):
    """Configure environment variables from a given configuration dictionary."""
    qt_plugin_path = os.path.join(qgis_main_path, "apps", "qt5", "plugins")
    qgis_bin_path = get_qgis_ltr(qgis_main_path, "bin")  # Assume get_qgis_path exists and handles input correctly
    qt_bin_path = os.path.join(qgis_main_path, "apps", "qt5", "bin")
    python_home_path = os.path.join(qgis_main_path, "apps", "Python39")
    python_path = os.path.join(qgis_main_path, "apps", "Python39", "lib", "site-packages")

    print(qt_plugin_path);
    print(qgis_bin_path);
    print(qt_bin_path);
    print(python_home_path);
    print(python_path);

    env_vars = {
        'QT_QPA_PLATFORM_PLUGIN_PATH': qt_plugin_path,
        'PYTHONHOME': python_home_path,
        'PYTHONPATH': python_path,
        'PATH': os.environ.get('PATH', '') + ";" + qgis_bin_path + ";" + qt_bin_path
    }
    for key, value in env_vars.items():
        set_environment_variable(key, value)

def xyz_tiler(config):
    print("Initializing QGIS paths...")
    configure_qgis_paths(config['qgis_main_path'])
    # Set environment variables for other QGIS and PyQt5 components
    print("Setting environment variables for QT and Python...")    
    configure_environment_variables(config['qgis_main_path'])
    print("DONE...")   

    # Import necessary libraries from QGIS Python API
    from qgis.analysis import QgsNativeAlgorithms
    from qgis.core import (
        QgsApplication,
        QgsProject,    
        QgsProcessingFeedback, 
        QgsRasterLayer,
        QgsCoordinateTransform,
        QgsCoordinateReferenceSystem
    )

    # Starting the QGIS application
    qgis_prefix_path = get_qgis_ltr(config['qgis_main_path'], "")
    QgsApplication.setPrefixPath(qgis_prefix_path, True)

    qgs = QgsApplication([], False) # QGIS is started without a GUI when set to False. If true, it opens a GUI.
    qgs.initQgis()
    
    # Loads the Processing framework.
    from qgis import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    #QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Load the raster layer from provided path and check its validity
    raster_file = config['xyz_raster_path'] # Raster file path.
    raster_layer = QgsRasterLayer(raster_file, "raster")

    if not raster_layer.isValid():
        print("Layer failed to load!")
        exit() 
    else:
        # Converts the current coordinate reference system of the raster layer to the target CRS.
        source_crs = raster_layer.crs()
        target_crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)
        transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
        # Converts the current extent of the layer.
        transformed_extent = transform.transformBoundingBox(raster_layer.extent())
        # Sets the EXTENT parameter using the converted extent.
        extent_str = "{},{},{},{}".format(transformed_extent.xMinimum(), transformed_extent.xMaximum(),transformed_extent.yMinimum(),  transformed_extent.yMaximum())
        extent_parameter = extent_str2= extent_str+' '+ '[EPSG:4326]'

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
            'EXTENT':extent_parameter,
            #'EXTENT': '26.973651074,27.002737108,39.455455330,39.472725163 [EPSG:4326]',
            'TMS_CONVENTION':config['xyz_tms_convention'],
            'HTML_TITLE':config['xyz_html_title'],
            'HTML_ATTRIBUTION':config['xyz_html_attribution'],
            'HTML_OSM':config['xyz_html_osm'],
            'OUTPUT_DIRECTORY': config['xyz_output_path'],
            'OUTPUT_HTML': config['xyz_output_path']+'/preview.html'
        }

        QgsProject.instance().setCrs(target_crs)
        QgsProject.instance().addMapLayer(raster_layer, True)
        # Starts process
        print("The XYZ Tile generation process is started. This may take some time, please be patient...")

        feedback = QgsProcessingFeedback()
        processing.run("qgis:tilesxyzdirectory", params, feedback=feedback)

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
