#!/usr/bin/env python3
"""
PNG to ICO Converter

A simple script to convert PNG files to ICO format using Pillow.
Supports multiple sizes for the ICO file and handles transparency.
"""

import os
import sys
from PIL import Image
import argparse


def convert_png_to_ico(input_path, output_path=None, sizes=None):
    """
    Convert a PNG file to ICO format.
    
    Args:
        input_path (str): Path to the input PNG file
        output_path (str): Path for the output ICO file (optional)
        sizes (list): List of sizes for the ICO file (default: [16, 32, 48, 64, 128, 256])
    
    Returns:
        str: Path to the created ICO file
    """
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.ico"
    
    try:
        # Open and load the PNG image (convert outside context manager to keep it in memory)
        img = Image.open(input_path)
        # Convert to RGBA if not already (to preserve transparency)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        # Load image data into memory
        img.load()
        
        # Create resized images for each size
        size_tuples = []
        for size in sizes:
            size_tuples.append((size, size))
        
        # Save as ICO file - save the first image with others appended
        # The sizes parameter must match the order of images provided
        img.save(
            output_path,
            sizes=size_tuples
        )
        
        # Close the original image
        img.close()
        
        print(f"Successfully converted '{input_path}' to '{output_path}'")
        print(f"Created ICO with sizes: {size_tuples}")
        return output_path
            
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        return None
    except Exception as e:
        print(f"Error converting file: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Convert PNG files to ICO format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python png_to_ico.py icon.png
  python png_to_ico.py icon.png -o custom_icon.ico
  python png_to_ico.py icon.png -s 16 32 48
  python png_to_ico.py icon.png --sizes 32 64 128 256
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the input PNG file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output ICO file path (default: same name as input with .ico extension)'
    )
    
    parser.add_argument(
        '-s', '--sizes',
        nargs='+',
        type=int,
        default=[16, 32, 48, 64, 128, 256],
        help='Sizes for the ICO file (default: 16 32 48 64 128 256)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    if not args.input_file.lower().endswith('.png'):
        print("Warning: Input file doesn't have a .png extension.")
    
    # Convert the file
    result = convert_png_to_ico(args.input_file, args.output, args.sizes)
    
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main() 