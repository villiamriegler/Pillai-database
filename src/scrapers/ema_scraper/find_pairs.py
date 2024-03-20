import os

# Directories containing the files
dir_sv = 'ema_sv' 
dir_en = 'ema_en' 

# Initialize a counter
counter = 0

# List to hold the common filenames without the last 6 characters
common_filenames = []

# Get the list of files in both directories without the last 6 characters
files_sv = {file[:-6]: file for file in os.listdir(dir_sv) if file.endswith('.pdf')}
files_en = {file[:-6]: file for file in os.listdir(dir_en) if file.endswith('.pdf')}

# Find common filenames (without the last 6 characters)
for name_sv in files_sv:
    if name_sv in files_en:
        # Increment the counter
        counter += 1
        # Add the filename to the common_filenames list
        common_filenames.append(name_sv)

# Save the common filenames to translations.py
with open('translations.txt', 'w') as f:
    # Write the common filenames
    for filename in common_filenames:
        f.write(f'{filename}\n')

# Output the total count
print(f'Total paired files: {counter}')

