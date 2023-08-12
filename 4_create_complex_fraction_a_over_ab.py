from PIL import Image
import numpy as np
import random
import os

def read_img_to_array(path_digit):
    """
    Read an image from the given path and convert it to a numpy array.

    Args:
        path_digit (str): Path to the image file.

    Returns:
        np.array: Numpy array representation of the image.
    """
    with Image.open(path_digit) as im:
        image_array = np.array(im)
    return image_array


def generate_fraction_array_a_over_ab(path_nume_a, path_deno_a, path_deno_b, path_bar, space_btw_ab):
    """
    Generate a 2D array (image representation) of a fraction of the form a/ab from provided image paths.
    
    Parameters:
    - path_nume_a (str): Path to the image representing the numerator "a".
    - path_deno_a (str): Path to the image representing the first part of the denominator "a".
    - path_deno_b (str): Path to the image representing the second part of the denominator "b".
    - path_bar (str): Path to the image of the fraction bar.
    - space_btw_ab (int): Space between the "a" and "b" parts of the denominator in pixels.
    
    Returns:
    - numpy.ndarray: A numpy array representing the fraction a/ab.
    """
    
    # Convert image paths to numpy arrays
    img_nume_a = read_img_to_array(path_nume_a)
    img_deno_a = read_img_to_array(path_deno_a)
    img_deno_b = read_img_to_array(path_deno_b)
    
    # Determine the width of the generated fraction based on the widest component
    col_num = max(img_nume_a.shape[1], img_deno_a.shape[1] + img_deno_b.shape[1])
    
    # Slightly extend the width for aesthetic purposes
    col_num = int(col_num * 1.4)
    
    # Resize the fraction bar to fit the computed width
    img_bar = Image.open(path_bar)
    width, height = img_bar.size
    img_resized = img_bar.resize((width, col_num))
    img_bar = np.array(img_resized)
    
    # Transpose the fraction bar (make it horizontal)
    img_bar = img_bar.T
    
    # Compute the total height of the resulting fraction array
    row_num = img_nume_a.shape[0] + img_deno_a.shape[0] + img_bar.shape[0]
    
    # Initialize the fraction array with zeros
    fraction_array = np.zeros((row_num, col_num), dtype=np.uint8)
    
    # Place numerator "a" in the fraction array
    offset = int((col_num - img_nume_a.shape[1]) / 2)
    for idx_r, row in enumerate(img_nume_a):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r][idx_c + offset] = pix
            
    # Place the fraction bar in the fraction array
    offset = int((col_num - img_bar.shape[1]) / 2)
    for idx_r, row in enumerate(img_bar):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r + img_nume_a.shape[0]][idx_c + offset] = pix
            
    # Place denominator part "a" in the fraction array
    offset = int(col_num / 2 - img_deno_a.shape[1]) - space_btw_ab
    for idx_r, row in enumerate(img_deno_a):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r + img_nume_a.shape[0] + img_bar.shape[0]][idx_c + offset] = pix
            
    # Place denominator part "b" in the fraction array
    offset = int(col_num / 2) + space_btw_ab
    for idx_r, row in enumerate(img_deno_b):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r + img_nume_a.shape[0] + img_bar.shape[0]][idx_c + offset] = pix
            
    return fraction_array


def run_multiple_times_a_over_ab(path_data, nume_a, deno_a, deno_b, space_btw_ab, num_sample, path_result):
    """
    Generate multiple image samples representing the fraction of the form a/ab using individual MNIST digits.

    Args:
        path_data (string): Directory where the individual processed MNIST digit images are stored.
        nume_a (int): The digit representing the numerator "a".
        deno_a (int): The digit representing the first part of the denominator "a".
        deno_b (int): The digit representing the second part of the denominator "b".
        space_btw_ab (int): Space in pixels between the "a" and "b" parts of the denominator.
        num_sample (int): The number of image samples to be generated.
        path_result (string): Directory where the generated fraction images will be saved.

    Procedure:
        For each sample:
        1. Randomly pick an image for each of the digits and the fraction bar from the provided data directory.
        2. Generate the fraction image using the chosen digit images.
        3. Save the resulting fraction image to the specified result directory.
    """
    
    for index in range(num_sample):
        # Construct the paths for the digit images and fraction bar image
        path_nume_a = path_data + str(nume_a) + '/' + random.choice(os.listdir(path_data + str(nume_a) + '/'))
        path_deno_a = path_data + str(deno_a) + '/' + random.choice(os.listdir(path_data + str(deno_a) + '/'))
        path_deno_b = path_data + str(deno_b) + '/' + random.choice(os.listdir(path_data + str(deno_b) + '/'))
        path_bar = path_data + 'one_as_fraction_bar/' + random.choice(os.listdir(path_data + 'one_as_fraction_bar/'))
        
        try:
            # Generate the fraction image using the selected images
            fraction_array = generate_fraction_array_a_over_ab(path_nume_a, path_deno_a, path_deno_b, path_bar, space_btw_ab)
            
            # Convert the array to an image
            img = Image.fromarray(fraction_array, 'L')  # 'L' indicates grayscale mode. Use 'RGB' for color images.
            
            # Save the generated image
            img.save(path_result + str(nume_a) + '_over_' + str(deno_a) + str(deno_b) + '_id_' + str(index) + '.jpg')
        except:
            # If an error occurs, skip to the next iteration
            continue

# settings 
numerator_a = 4
denominator_a = 9
denominator_b = 2
space_btw_ab = 1
num_sample = 20
path_data = './digits/processed/'
path_result = './fractions/'
os.makedirs(path_result, exist_ok=True)
run_multiple_times_a_over_ab(path_data, numerator_a, denominator_a, denominator_b, space_btw_ab, num_sample, path_result)