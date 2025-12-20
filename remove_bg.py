from PIL import Image
import os
import sys

def remove_background(image_path, tolerance=60):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        datas = img.getdata()

        # Sample the background color from top-left pixel
        bg_color = datas[0]
        print(f"Sampling background color: {bg_color}")

        new_data = []
        for item in datas:
            # item is (r, g, b, a)
            # Calculate distance to background color
            diff = sum(abs(item[i] - bg_color[i]) for i in range(3))
            
            # Additional check: if it's very green
            is_green = item[1] > item[0] + 30 and item[1] > item[2] + 30
            
            if diff < tolerance or is_green:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item)

        img.putdata(new_data)
        
        # Save as PNG
        base = os.path.splitext(image_path)[0]
        output_path = base + "_transparent.png"
        img.save(output_path, "PNG")
        print(f"Success: {output_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_bg.py <image_path>")
    else:
        remove_background(sys.argv[1])
