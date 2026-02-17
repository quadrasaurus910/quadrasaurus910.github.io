import sys
import os
from PIL import Image

def process_image(file_path):
    # 1. Validate file and naming
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    base_name = os.path.splitext(file_path)[0]
    output_path = f"{base_name}_binary.txt"

    try:
        # 2. Open image and ensure it's RGBA
        img = Image.open(file_path).convert("RGBA")
        width, height = img.size
        pix = img.load()
        totalZ = 0
        totalO = 0

        print(f"Processing {width}x{height} image...")
        print("-" * 30)

        binary_rows = []

        # 3. Iterate and print "live" stats
        for y in range(height):
            row_data = []
            ones = 0
            zeros = 0

            for x in range(width):
                # We only care about the Alpha channel (index 3)
                # 0 = Transparent, 1 = Any level of opacity
                is_opaque = 1 if pix[x, y][3] > 0 else 0
                row_data.append(str(is_opaque))
                
                if is_opaque:
                    ones += 1
                    totalO += 1
                else:
                    zeros += 1
                    totalZ+= 1
            
            # Print live data for each line
            # print(f"Row {y:03d}: {ones:4d} [1s] | {zeros:4d} [0s]")
            
            # Store the row as a string of 1s and 0s
            binary_rows.append("".join(row_data))

        # 4. Save to file
        with open(output_path, "w") as f:
            f.write("\n".join(binary_rows))

        print("-" * 30)
        print(f"Success! Binary map saved to: {output_path}")
        print(f"Total ones: {totalO}, total zeros: {totalZ}, Total combined: {totalO + totalZ}  ")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py your_image.png")
    else:
        process_image(sys.argv[1])
