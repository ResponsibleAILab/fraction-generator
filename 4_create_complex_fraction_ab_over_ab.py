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

def generate_fraction_array_ab_over_ab(path_nume_a, path_nume_b, path_deno_a, path_deno_b, path_bar, space_btw_ab):
    """
    Generate a fraction image with the format ab/cd.

    Args:
        path_nume_a (str): Path to image of numerator's first digit.
        path_nume_b (str): Path to image of numerator's second digit.
        path_deno_a (str): Path to image of denominator's first digit.
        path_deno_b (str): Path to image of denominator's second digit.
        path_bar (str): Path to image of the fraction bar.
        space_btw_ab (int): Space between the digits A and B or C and D.

    Returns:
        np.array: Numpy array representation of the fraction image.
    """
    # Load the digit images into numpy arrays
    img_nume_a = read_img_to_array(path_nume_a)
    img_nume_b = read_img_to_array(path_nume_b)
    img_deno_a = read_img_to_array(path_deno_a)
    img_deno_b = read_img_to_array(path_deno_b)

    # Calculate the maximum column width needed, allowing some scaling factor (1.4 in this case)
    col_num = max(img_nume_a.shape[1] + img_nume_b.shape[1], img_deno_a.shape[1] + img_deno_b.shape[1])
    col_num = int(col_num * 1.4)

    # Resize the fraction bar to span the width
    img_bar = Image.open(path_bar)
    width, height = img_bar.size
    img_resized = img_bar.resize((width, col_num))
    img_bar = np.array(img_resized)
    img_bar = img_bar.T

    # Initialize the resulting fraction image
    row_num = img_nume_a.shape[0] + img_deno_a.shape[0] + img_bar.shape[0]
    fraction_array = np.zeros((row_num, col_num), dtype=np.uint8)

    # Add the numerator (digits A and B)
    # Position A
    offset = int(col_num/2 - img_nume_a.shape[1]) - space_btw_ab
    for idx_r, row in enumerate(img_nume_a):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r][idx_c+offset] = pix
    # Position B
    offset = int(col_num/2) + space_btw_ab
    for idx_r, row in enumerate(img_nume_b):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r][idx_c+offset] = pix

    # Add the fraction bar
    offset = int((col_num-img_bar.shape[1])/2)
    for idx_r, row in enumerate(img_bar):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r+img_nume_a.shape[0]][idx_c+offset] = pix

    # Add the denominator (digits C and D)
    # Position C
    offset = int(col_num/2-img_deno_a.shape[1]) - space_btw_ab
    for idx_r, row in enumerate(img_deno_a):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r+img_nume_a.shape[0]+img_bar.shape[0]][idx_c+offset] = pix
    # Position D
    offset = int(col_num/2) + space_btw_ab
    for idx_r, row in enumerate(img_deno_b):
        for idx_c, pix in enumerate(row):
            fraction_array[idx_r+img_nume_a.shape[0]+img_bar.shape[0]][idx_c+offset] = pix

    return fraction_array

def run_multiple_times_ab_over_ab(path_data, nume_a, nume_b, deno_a, deno_b, space_btw_ab, num_sample, path_result):
    """
    Generate and save multiple samples of fraction images with the format ab/cd.

    Args:
        path_data (str): Directory of the individual processed MNIST data.
        nume_a (int): First digit of the numerator.
        nume_b (int): Second digit of the numerator.
        deno_a (int): First digit of the denominator.
        deno_b (int): Second digit of the denominator.
        space_btw_ab (int): Space between the digits in the numerator or denominator.
        num_sample (int): Number of fraction images to generate.
        path_result (str): Directory to save the generated fraction images.
    """
    for index in range(num_sample):
        # Randomly choose image paths for each of the digits and the fraction bar
        path_nume_a = path_data + str(nume_a) + '/' + random.choice(os.listdir(path_data + str(nume_a) + '/'))
        path_nume_b = path_data + str(nume_b) + '/' + random.choice(os.listdir(path_data + str(nume_b) + '/'))
        path_deno_a = path_data + str(deno_a) + '/' + random.choice(os.listdir(path_data + str(deno_a) + '/'))
        path_deno_b = path_data + str(deno_b) + '/' + random.choice(os.listdir(path_data + str(deno_b) + '/'))
        path_bar = path_data + 'one_as_fraction_bar/' + random.choice(os.listdir(path_data + 'one_as_fraction_bar/'))

        # Generate the fraction image
        fraction_array = generate_fraction_array_ab_over_ab(path_nume_a, path_nume_b, path_deno_a, path_deno_b, path_bar, space_btw_ab)
        img = Image.fromarray(fraction_array, 'L')  # 'L' indicates grayscale mode. Use 'RGB' for color images.
        img.save(path_result + str(nume_a) + str(nume_b) + '_over_' + str(deno_a)+ str(deno_b) + '_id_' + str(index) + '.jpg')

# Parameters for generating fraction images
numerator_a = 4
numerator_b = 1
denominator_a = 9
denominator_b = 2
space_btw_ab = 1
num_sample = 10
path_data = './digits/processed/'
path_result = './fractions/'
os.makedirs(path_result, exist_ok=True)

# Generate and save the fraction images
run_multiple_times_ab_over_ab(path_data, numerator_a, numerator_b, denominator_a, denominator_b, space_btw_ab, num_sample, path_result)