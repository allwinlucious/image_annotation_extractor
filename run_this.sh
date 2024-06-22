#!/bin/bash

# Directory containing JPG files
directory="./images_in_this"

# Iterate through each JPG file in the directory
for file in "$directory"/*.jpg; do
    echo "Processing $file"
    # Check if there are any JPG files
    if [ -f "$file" ]; then
        # Extract the filename without the path
        filename=$(basename -- "$file")

        # Step 1: Delete 'cropped_images' folder if it exists
        folder_to_delete="cropped_images"
        if [ -d "$folder_to_delete" ]; then
            rm -rf "$folder_to_delete"
        fi

        # Step 2: Run find_annotations.py with the current filename
        python3 find_annotations.py "$filename"

        # Step 3: Delete 'thresholded_images' folder if it exists
        folder_to_delete="thresholded_images"
        if [ -d "$folder_to_delete" ]; then
            rm -rf "$folder_to_delete"
        fi

        # Step 4: Run white_threshold.py
        python3 white_threshold.py

        # Step 5: Run perform_ocr.py
        python3 perform_ocr.py
    fi
done
