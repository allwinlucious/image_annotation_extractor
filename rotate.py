import os
import cv2
import numpy as np

# Function to rotate image to make green line horizontal
def rotate_image_to_horizontal(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Adjust file extensions as necessary
            # Read the image
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # Convert to HSV color space for better color segmentation
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Define range of green color in HSV
            lower_green = np.array([40, 40, 40])  # Adjust these values to your specific shade of green
            upper_green = np.array([80, 255, 255])

            # Threshold the HSV image to get only green colors
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Assume the largest contour is our green line
            largest_contour = max(contours, key=cv2.contourArea)

            # Fit a line to the contour
            vx, vy, _, _ = cv2.fitLine(largest_contour, cv2.DIST_L2, 0, 0.01, 0.01)

            # Calculate angle of the line
            angle = np.arctan2(vy, vx) * 180 / np.pi
            print(f"Angle: {angle}")

            # Rotate image to make the line horizontal
            rotated = rotate_image(img, angle)

            # Save the rotated image to output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, rotated)

            print(f"Processed {filename} and saved to {output_path}")

def rotate_image(image, angle):
    # Ensure angle is float
    angle = float(angle)
    
    # Rotate the image by the specified angle
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (cols, rows))
    return rotated


input_folder = './cropped_images'
output_folder = './rotated_images'
rotate_image_to_horizontal(input_folder, output_folder)
