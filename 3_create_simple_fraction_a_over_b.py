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

def generate_fraction_array_a_over_b(path_nume, path_deno, path_bar):
    """
    Generate a fraction representation in the format "a/b" using given image paths.

    Args:
        path_nume (str): Path to the image of the numerator.
        path_deno (str): Path to the image of the denominator.
        path_bar (str): Path to the image of the fraction bar.

    Returns:
        np.array: Numpy array representing the fraction "a/b".
    """
    # Load the images into numpy arrays
    img_nume = read_img_to_array(path_nume)
    img_deno = read_img_to_array(path_deno)
    img_bar = read_img_to_array(path_bar)
    img_bar = img_bar.T  # transpose the fraction bar

    # Calculate the dimensions for the final fraction image
    row_num = img_nume.shape[0] + img_deno.shape[0] + img_bar.shape[0]
    col_num = max(img_nume.shape[1], img_deno.shape[1], img_bar.shape[1])

    # Initialize a blank image array
    fraction_array = np.zeros((row_num, col_num), dtype=np.uint8)

    # Position and merge the numerator image
    offset = int((col_num - img_nume.shape[1]) / 2)
    for idx_r, row in enumerate(img_nume):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r][idx_c + offset] = pix

    # Position and merge the fraction bar image
    offset = int((col_num - img_bar.shape[1]) / 2)
    for idx_r, row in enumerate(img_bar):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r + img_nume.shape[0]][idx_c + offset] = pix

    # Position and merge the denominator image
    offset = int((col_num - img_deno.shape[1]) / 2)
    for idx_r, row in enumerate(img_deno):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r + img_nume.shape[0] + img_bar.shape[0]][idx_c + offset] = pix

    return fraction_array

def run_multiple_times_a_over_b(path_data, numerator, denominator, num_sample, path_result):
    """
    Generate multiple samples of fraction representations using given numbers.

    Args:
        path_data (str): Directory of the individual processed MNIST data.
        numerator (int): Numerator of the fraction.
        denominator (int): Denominator of the fraction.
        num_sample (int): Number of fraction samples to generate.
        path_result (str): Directory to save the generated fraction images.
    """
    for index in range(num_sample):
        # Select random images for numerator, denominator, and fraction bar
        path_nume = path_data + str(numerator) + '/' + random.choice(os.listdir(path_data + str(numerator) + '/'))
        path_deno = path_data + str(denominator) + '/' + random.choice(os.listdir(path_data + str(denominator) + '/'))
        path_bar = path_data + 'one_as_fraction_bar/' + random.choice(os.listdir(path_data + 'one_as_fraction_bar/'))

        fraction_array = generate_fraction_array_a_over_b(path_nume, path_deno, path_bar)
        
        # Convert the numpy array to an image and save it
        img = Image.fromarray(fraction_array, 'L')  # 'L' indicates grayscale mode.
        img.save(path_result + str(numerator) + '_over_' + str(denominator) + '_id_' + str(index) + '.jpg')

# Define values for numerator, denominator, number of samples, data path, and result path
numerator = 4
denominator = 9
num_sample = 10
path_data = './digits/processed/'
path_result = './fractions/'

# Create the result directory if it doesn't exist
os.makedirs(path_result, exist_ok=True)

# Generate fraction images
run_multiple_times_a_over_b(path_data, numerator, denominator, num_sample, path_result)
