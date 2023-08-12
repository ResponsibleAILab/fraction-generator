import os
from PIL import Image
import numpy as np

list_number = [i for i in range(10)]

for number in list_number:
    
    # Define paths for the raw digit images and the processed digit images
    path_digit = './digits/raw/' + str(number) + '/'
    path_output = './digits/processed/' + str(number) + '/'
    
    # Create the output directory if it doesn't exist
    os.makedirs(path_output, exist_ok=True)
    
    # List all image files in the raw digit directory
    list_img = os.listdir(path_digit)
    
    for img_name in list_img:
        try:
            # Open an image file
            with Image.open(path_digit + img_name) as im:
                # Convert image to numpy array
                image_array = np.array(im)
            
            # Initialize indices for trimming the image's left and right boundaries
            left_index = len(image_array) 
            right_index = 0
            
            # Loop through each row of the image array
            for i in range(len(image_array)):
                row = image_array[i]
                
                # Find indices of pixels with a value greater than 100
                indices = [i for i, x in enumerate(row) if x > 100]
                
                if indices:
                    first_index = indices[0]
                    last_index = indices[-1]
                    
                    # Adjust the left boundary index if necessary
                    if first_index < left_index:
                        if row[first_index-1] > 20:
                            left_index = first_index-1
                        else:
                            left_index = first_index
                    
                    # Adjust the right boundary index if necessary
                    if last_index > right_index:
                        if row[last_index+1] > 20:
                            right_index = last_index+1
                        else:
                            right_index = last_index
            
            # Display the determined left and right indices
            print('left_index: {}'.format(left_index))
            print('right_index: {}'.format(right_index))

            # Extract the values between the determined left and right boundaries
            extracted_values = image_array[:, left_index:right_index]
            trans_array = extracted_values
            # Uncomment the following line to invert colors (if needed)
            # trans_array = 255 - extracted_values
            
            # Convert the NumPy array back to an image
            img = Image.fromarray(trans_array, 'L')  # 'L' indicates grayscale mode. Use 'RGB' for color images.
            
            # Save the processed image to the output directory
            img.save(path_output + img_name)
            
            # Print the shape of the original image array
            print(image_array.shape)
        
        # Handle exceptions
        except:
            print('errors occur: {}'.format(path_digit + img_name))
