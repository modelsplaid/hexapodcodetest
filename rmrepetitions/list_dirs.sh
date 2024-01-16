#!/bin/bash

get_folder_lst() {
    # Check if a path is provided
    if [ -z "$1" ]
    then
        echo "Folder seraching path: ./ "
        search_path=./
    else
        search_path=$1

    fi
    #declare -g found_lst
    # List all folders in the provided path
    declare -g directories=()

    # Use while loop and read to correctly handle directory names with spaces
    while IFS= read -r dir; do
        directories+=("$dir")  # Append each directory to the array
    done < <(find "$search_path" -type d)

    # Now you can iterate over the array and access each directory name
    for dir in "${directories[@]}"; do
        echo "$dir"
    done

}

get_folder_lst


# Example array
my_array=("${directories[@]}")

# Get the length of the array
array_length=${#my_array[@]}
echo array_length: $array_length

# Iterate over the array
for (( i=0; i<array_length; i++ )); do
    # Print the current state of the array
    #echo "${my_array[@]}"
    echo "${my_array[@]}"

    # Remove the first element
    unset my_array[0] # Remove the first element
    my_array=("${my_array[@]}") # Re-index the array
done
