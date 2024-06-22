import cv2
import numpy as np
import os
import sys

# Load the image
image_path = "./images_in_this/"+sys.argv[1]
image = cv2.imread(image_path)

# Check if the image was successfully loaded
if image is None:
    print(f"Error: Unable to load image from {image_path}")
    exit()

# Convert BGR to RGB for matplotlib compatibility
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of green color in HSV
lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])

# Threshold the HSV image to get only green colors
mask = cv2.inRange(hsv, lower_green, upper_green)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define padding around the detected green segment
padding_x = 40  # Example padding
padding_y = 40  # Example padding





# Create a directory to save cropped images
output_dir = 'cropped_images'
os.makedirs(output_dir, exist_ok=True)

# List to store non-overlapping bounding boxes
bounding_boxes = []

# Iterate over all contours (green segments)
for contour in contours:
    # Calculate bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)
    
    # Add padding to the bounding box
    x -= padding_x
    y -= padding_y
    w += 2 * padding_x
    h += 2 * padding_y
    
    # Ensure the cropped area is within image bounds
    x = max(x, 0)
    y = max(y, 0)
    
    # Check for overlapping bounding boxes
    overlap = False
    for (x_, y_, w_, h_) in bounding_boxes:
        if x < x_ + w_ and x + w > x_ and y < y_ + h_ and y + h > y_:
            overlap = True
            # Keep the bounding box with the largest area
            if w * h > w_ * h_:
                bounding_boxes.remove((x_, y_, w_, h_))
                bounding_boxes.append((x, y, w, h))
            break
    
    if not overlap:
        bounding_boxes.append((x, y, w, h))
    
# Iterate over non-overlapping bounding boxes
for i, (x, y, w, h) in enumerate(bounding_boxes):
    # Draw bounding box on the original image
    cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 0, 255), 2)
    



    # Crop the original image around the ROI
    cropped_image = image_rgb[y:y+h, x:x+w]
    
    # Save the cropped image to a folder
    output_file = os.path.join(output_dir, f'cropped_{i + 1}.png')
    cv2.imwrite(output_file, cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))
    print(f"Cropped image saved as {output_file}")
