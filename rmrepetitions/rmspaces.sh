#!/bin/bash

# Check if a path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path>"
    exit 1
fi

# Navigate to the given directory
cd "$1"

# Check if the directory change was successful
if [ $? -ne 0 ]; then
    echo "Error: Unable to access directory $1"
    exit 1
fi

# Loop over the files with spaces in their names
find . -maxdepth 1  -not -name ".*"  | while IFS= read -r file; do
    # Replace spaces with underscores (or any other character)
    new_name=$(echo "$file" | tr ' ' '_')
    mv "$file" "$new_name"
done

echo "Spaces in filenames have been replaced with underscores."
