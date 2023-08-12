 **MNIST Fraction Generation**

This repository provides a set of Python scripts that make use of the MNIST dataset to create and manipulate fractions represented by the dataset's digits.

**Table of Contents**

1. [Scripts Overview](#scripts-overview)
2. [Dependencies](#dependencies)
3. [Getting Started](#getting-started)
4. [Usage](#usage)

**Scripts Overview**

**1.**  **1\_determine\_bbox\_4\_each\_digit\_in\_mnist.py**

This script determines the bounding box for each digit in the MNIST dataset. This is essential for aligning the digits properly when forming fractions.

**2.**  **2\_use\_1\_to\_serve\_fraction\_bar.py**

Utilizes the output from the first script (bounding boxes) to create a fraction bar that will be placed between the numerator and the denominator.

**3.**  **3\_create\_simple\_fraction\_a\_over\_b.py**

Forms a simple fraction with a single-digit numerator (a) and a single-digit denominator (b) using the MNIST digits and the fraction bar from the previous script.

**4.**  **4\_create\_complex\_fraction\_a\_over\_ab.py**

Constructs a complex fraction with a single-digit numerator (a) and a two-digit denominator (ab) using the MNIST digits.

**5.**  **4\_create\_complex\_fraction\_ab\_over\_ab.py**

Creates a complex fraction where both the numerator and the denominator have two digits (ab/ab) using the MNIST digits.

**Dependencies**

- Python 3.x
- Libraries:
  - Numpy
  - Matplotlib
  - (any other libraries required by the code, e.g., TensorFlow or PyTorch if using them for MNIST)

**Getting Started**

1. Clone this repository:
```
git clone https://github.com/ResponsibleAILab/fraction-generator
```

2. Install the required dependencies:
```
pip install numpy matplotlib(other libraries)
```

**Usage**

To use any of the scripts, navigate to the script directory and run them as follows:

1. Determine bounding boxes:
```
python 1_determine_bbox_4_each_digit_in_mnist.py
```
2. Create the fraction bar:
```
python 2_use_1_to_serve_fraction_bar.py
```
3. Generate a simple fraction:
```
python 3_create_simple_fraction_a_over_b.py
```
4. Generate a complex fraction with a single-digit numerator:
```
python 4_create_complex_fraction_a_over_ab.py
```
5. Generate a complex fraction with two-digit numerator and denominator:
```
python 4_create_complex_fraction_ab_over_ab.py
```
Feel free to modify the scripts or use them as part of larger projects. If you encounter any issues or have suggestions for improvements, please open an issue on this repository.
