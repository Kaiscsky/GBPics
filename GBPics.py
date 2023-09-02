import numpy as np
from PIL import Image

img = Image.open('filename.jpg')    # Opens input file
img_rgb = img.convert('RGB')
img_input = np.array(img_rgb)
img_output = np.zeros((144, 160, 3), dtype=np.uint8)    # Creates array for output at Gameboy resolution

# Change for different results, minimum value is 1.
# Alters how many neighboring pixels in the input image will be averaged.
x_depth = 1
y_depth = 1

# Change for different results, values can be between 0 and 255, increasing.
# Alters the thresholds between colors
dark_bound = 64
middle_bound = 128
light_bound = 191

img_height = img_input.shape[0]
img_width = img_input.shape[1]
y_gap = img_height / img_output.shape[0]    # The approximate gaps between output pixels when
x_gap = img_width / img_output.shape[1]     # spread out on the input image
c0 = [15, 56, 15]       # Darkest Color
c1 = [48, 98, 48]
c2 = [139, 172, 15]
c3 = [155, 188, 15]     # Lightest Color

for i in range(img_output.shape[0]):    # Commenting this is left as an exercise for the reader
    for j in range(img_output.shape[1]):
        center_y = round(i * y_gap)
        center_x = round(j * x_gap)
        avg = 0
        for n in [y - y_depth + 1 for y in range(y_depth * 2 - 1)]:     # This appeared to me in a vision
            for m in [x - x_depth + 1 for x in range(x_depth * 2 - 1)]:
                if (center_y + n < img_height) and\
                        (center_y + n >= 0) and\
                        (center_x + m < img_width) and\
                        (center_x + m >= 0):
                    avg += sum(img_input[center_y + n, center_x + m]) / 3
        avg = avg/((x_depth * 2 - 1) * (y_depth * 2 - 1))
        if avg < dark_bound:
            img_output[i, j] = c0
        elif avg < middle_bound:
            img_output[i, j] = c1
        elif avg < light_bound:
            img_output[i, j] = c2
        else:
            img_output[i, j] = c3

img_new = Image.fromarray(img_output)       # Create a PIL image
img_new.show()                              # View in default viewer
img_new.save("filename_gb.png")             # Save image
