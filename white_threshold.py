import os
import cv2
import numpy as np

# Function to process images
def process_image(input_path, output_path):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust based on your image file extensions
            # Read the image
            image_path = os.path.join(input_path, filename)
            image = cv2.imread(image_path)

            # Define thresholds for each channel
            lower_white = np.array([200, 200, 200])  # Example threshold for each channel (adjust as needed)
            upper_white = np.array([255, 255, 255])

            # Create mask for white pixels
            mask = cv2.inRange(image, lower_white, upper_white)

            # Apply mask to original image
            result = cv2.bitwise_and(image, image, mask=mask)

            # Save the result image to output folder
            output_file_path = os.path.join(output_path, filename)
            cv2.imwrite(output_file_path, result)

            print(f"Processed: {filename}")

# Example usage:
input_folder = './cropped_images'  # Replace with your input folder path
output_folder = './thresholded_images'  # Replace with your output folder path

process_image(input_folder, output_folder)
