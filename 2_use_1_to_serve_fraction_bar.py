from PIL import Image
import numpy as np
import os
import shutil

# Specify the number to be processed (in this case, digit "1")
number = 1 

# Define paths for the processed digit images and the destination directory
path_digit = './digits/processed/' + str(number) + '/'
path_output = './digits/processed/one_as_fraction_bar/'

# Create the output directory if it doesn't exist
os.makedirs(path_output, exist_ok=True)

# List all image files in the processed digit directory
list_img = os.listdir(path_digit)

# Iterate through each image in the directory
for img_name in list_img:
    # Open an image file
    with Image.open(path_digit + img_name) as im:
        # Convert image to numpy array
        image_array = np.array(im)

    # Determine the number of columns (width) in the image
    num_columns = image_array.shape[1]

    # Check if the width of the digit 1 image is less than 5 pixels.
    # This condition assumes that a straight-up digit "1" will have a small width.
    if num_columns < 5:
        # Convert the NumPy array back to an image
        img = Image.fromarray(image_array, 'L')  # 'L' indicates grayscale mode. Use 'RGB' for color images.
        
        # Define the source and destination paths for copying
        source_path = path_digit + img_name
        destination_path = path_output + img_name
        
        # Copy the up-straight digit "1" images to a new directory
        shutil.copy(source_path, destination_path)
