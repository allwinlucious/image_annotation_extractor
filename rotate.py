import cv2
import numpy as np
import os

# Function to rotate image to make the largest green line horizontal
def rotate_to_horizontal(image):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (green line)
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate minimum area bounding rectangle
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Find the angle to rotate such that the largest green line becomes horizontal
    angle = rect[2]
    if rect[1][0] < rect[1][1]:  # If width < height, add 90 degrees
        angle += 90

    # Get the rotation matrix for the angle
    M = cv2.getRotationMatrix2D(rect[0], angle, 1.0)

    # Rotate the original image
    rotated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return rotated

# Path to folder containing cropped images
folder_path = 'cropped_images/'

# Iterate over all images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # Load image
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Unable to load image {filename}")
            continue

        # Rotate image to make largest green line horizontal
        rotated_image = rotate_to_horizontal(image)

        # Save rotated image
        output_path = os.path.join(folder_path, f'rotated_{filename}')
        cv2.imwrite(output_path, rotated_image)
        print(f"Rotated image saved as {output_path}")
