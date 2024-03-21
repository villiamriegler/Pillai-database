import os

# Directories containing the files
DIR_SV = 'ema_sv' 
DIR_EN = 'ema_en' 
OUTPUT_FILE_NAME = 'translations.txt'
NUMBER_OF_IGNORED_CHARS = -6

# Initialize a counter for number of found pairs
counter = 0

# List to hold the common filenames without the last 6 characters
common_filenames = []

# Get the list of files in both directories without the last 6 characters
files_sv = {file[:NUMBER_OF_IGNORED_CHARS]: file for file in os.listdir(DIR_SV) if file.endswith('.pdf')}
files_en = {file[:NUMBER_OF_IGNORED_CHARS]: file for file in os.listdir(DIR_EN) if file.endswith('.pdf')}

# Find common filenames (without the last 6 characters)
for name_sv in files_sv:
    if name_sv in files_en:
        # Increment the counter
        counter += 1
        # Add the filename to the common_filenames list
        common_filenames.append(name_sv)

# Save the common filenames to translations.py
with open(OUTPUT_FILE_NAME, 'w') as f:
    # Write the common filenames
    for filename in common_filenames:
        f.write(f'{filename}\n')

# Output the total count
print(f'Total paired files: {counter}')

