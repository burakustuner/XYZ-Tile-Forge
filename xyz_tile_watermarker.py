"""
/***************************************************************************
                                XYZ Tile Watermarker
 Adds watermarks to generated XYZ tiles for copyright or branding purposes.

 The XYZ Tile Watermarker script facilitates the addition of custom text watermarks
 to tiles within specified zoom levels. This is especially useful for copyright
 protection, branding, or adding any pertinent information directly onto the map tiles.
 The script supports customization of the watermark text, font, size, color, and positioning,
 as well as the frequency of watermark application across the tiles.

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
    - Ensure the Pillow library (PIL) is installed for image processing.
    - Configure the script with paths, watermark text, font details, and
      other parameters to match your specific requirements.
    - Run the script to apply watermarks to your tiles. The script processes
      each tile within the specified zoom levels, adding watermarks according
      to the configured frequency.

Parameters:
    config (dict): Configuration parameters for watermarking tiles.
        - watermark_directory: Directory containing the tile images to be watermarked.
        - watermark_text: Text to be used as the watermark.
        - watermark_layer_levels: List of zoom levels to which watermarks will be applied.
        - watermark_font_path: Path to the font file for the watermark text.
        - watermark_font_size: Font size for the watermark text.
        - watermark_text_color: Color of the watermark text (RGBA).
        - watermark_margin_left: Left margin for the watermark text positioning.
        - watermark_margin_bottom: Bottom margin for the watermark text positioning.
        - watermark_frequency: Frequency of watermarking tiles (e.g., every 5th tile).

Notes:
    - The ability to apply watermarks selectively based on zoom level and frequency
      allows for optimized processing and customization to meet various project needs.
    - It is recommended to review the output to ensure watermarks do not obscure
      important tile details and are in compliance with copyright laws.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def xyz_tile_watermarker(config):
    watermark_directory = config['watermark_directory']
    watermark_text = config['watermark_text']
    watermark_layer_levels = config['watermark_layer_levels']
    watermark_font_path = config['watermark_font_path']
    watermark_font_size = config['watermark_font_size']
    watermark_text_color = config['watermark_text_color']
    watermark_margin_left = config['watermark_margin_left']
    watermark_margin_bottom = config['watermark_margin_bottom']
    watermark_frequency = config['watermark_frequency']

    # Function to add watermark to an image
    def add_watermark_to_image(image_path, text, position, font, color):
        with Image.open(image_path) as img:
            drawable = ImageDraw.Draw(img)
            drawable.text(position, text, fill=color, font=font)
            img.save(image_path)

    # Function to process all images in a directory
    def process_directory(directory):
        for root, dirs, files in os.walk(directory):
            for index, filename in enumerate(files):
                # Apply watermark only to specific file types and based on the frequency config               
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and index % watermark_frequency == 0:
                    file_path = os.path.join(root, filename)
                    try:
                        font = ImageFont.truetype(watermark_font_path, watermark_font_size)
                    except IOError:
                        font = ImageFont.load_default()
                        print("Fallback to default font.")

                    img = Image.open(file_path)

                    position = (watermark_margin_left, img.height - watermark_margin_bottom)
                    add_watermark_to_image(file_path, watermark_text, position, font, watermark_text_color)
                    img.close()
                    print(f"Watermark added to {file_path}")

    # Process each zoom level directory
    for level in watermark_layer_levels:
        level_path = os.path.join(watermark_directory, str(level))
        if os.path.exists(level_path):
            print(f"Processing zoom level {level}...")
            process_directory(level_path)
        else:
            print(f"Zoom level {level} directory does not exist. Skipping...")

    print("Watermarking process completed.")

if __name__ == "__main__":
    # Example configuration for testing
    config = {
        'watermark_directory': "path/to/output/directory",
        'watermark_text': "@2024",
        'watermark_layer_levels': [14,15,17],
        'watermark_font_path': "arial.ttf",
        'watermark_font_size': 15,
        'watermark_text_color': (255, 255, 255, 10),  # RGBA
        'watermark_margin_left': 10,
        'watermark_margin_bottom': 10,
        'watermark_frequency': 5
    }
    xyz_tile_watermarker(config)
