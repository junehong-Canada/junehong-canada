from PIL import Image
import os
import sys

def resize_by_percentage(input_path, percentage):
    """Resizes an image by a given percentage."""
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    try:
        with Image.open(input_path) as img:
            width, height = img.size
            scale = percentage / 100.0
            new_width = int(width * scale)
            new_height = int(height * scale)

            # Use Resampling.LANCZOS for high quality (requires Pillow >= 9.0.0)
            # Fallback for older Pillow versions
            resample_method = getattr(Image, 'Resampling', Image).LANCZOS
            
            resized_img = img.resize((new_width, new_height), resample_method)

            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_small{ext}"

            resized_img.save(output_path)
            print(f"Resized '{input_path}' to {percentage}% ({new_width}x{new_height})")
            print(f"Saved as '{output_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check for command line arguments, otherwise ask for input
    input_file = sys.argv[1] if len(sys.argv) > 1 else input("Enter image filename: ")
    ratio_val = sys.argv[2] if len(sys.argv) > 2 else input("Enter resize percentage (e.g. 50): ")
    
    resize_by_percentage(input_file, float(ratio_val))
