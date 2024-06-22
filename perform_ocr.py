import os
import cv2
import easyocr
import numpy as np
import re
import csv
import sys
# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Replace 'en' with the language(s) you want to recognize

# Function to remove non-numeric characters
def remove_non_numeric(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    return re.sub(r'[a-zA-Z]', '', cleaned_text)

# Function to process each image
def process_image(image_path):
    # Read image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Perform OCR using EasyOCR
    result = reader.readtext(image)

    # Sort detections by their top-left corner coordinates (x1, y1)
    sorted_result = sorted(result, key=lambda x: x[0][0][0])  # Sort by x-coordinate of top-left corner

    # Merge detections that are close in location
    merged_text = ""
    previous_box = None
    for detection in sorted_result:
        box = detection[0]
        text = detection[1]
        
        if previous_box is None:
            merged_text += text 
        else:
            # Check if the current box overlaps or is close to the previous box
            x1_curr, y1_curr, x2_curr, y2_curr = box
            x1_prev, y1_prev, x2_prev, y2_prev = previous_box
            
            if x1_curr > x2_prev:  # New line or significant gap detected
                merged_text = merged_text.strip()  + text 
            else:  # Merge text in the same line or close proximity
                merged_text +=  text
        
        # Update previous_box to current box for the next iteration
        previous_box = box
    
    cleaned_text = remove_non_numeric(merged_text).strip()
    return cleaned_text

# Path to the folder containing images
folder_path = './thresholded_images'  # Replace with your folder path

# Path to the output CSV file
output_csv = './result.csv'  # Replace with your desired output CSV file path

# Initialize a list to collect all cleaned text
all_cleaned_text = [sys.argv[1]]

# Iterate through images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_path, filename)
        cleaned_text = process_image(image_path)
        all_cleaned_text.append(cleaned_text)

# Print the cleaned OCR results as a single row
print('\033[92m'+' , '.join(all_cleaned_text)+'\033[0m')

# Write the single row to the CSV file
with open(output_csv, mode='a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(all_cleaned_text)

