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
    done < <(find "$search_path" -maxdepth 1 -type d)

    # Remove the first element
    unset directories[0] # Remove the first element
    directories=("${directories[@]}") # Re-index the array

    # Now you can iterate over the array and access each directory name
    # for dir in "${directories[@]}"; do
    #     echo "$dir"
    # done

}

loop_folder_lst() {
    directories=$1
    dirs_arr=("${directories[@]}")

    # Get the length of the array
    array_length=${#dirs_arr[@]}
    echo Found number of directories: $array_length

    # Iterate over the array
    for (( i=0; i<array_length; i++ )); do
        # Print the current state of the array

        # Get first dir
        fst_dir=$dirs_arr

        # Remove the first element
        unset dirs_arr[0] # Remove the first element
        dirs_arr=("${dirs_arr[@]}") # Re-index the array
    
        # loop over remain 
        for one_dir in ${dirs_arr[@]}; do
            # replace spaces 
            
            # rm repetitions
            bash rmrep.sh $fst_dir $one_dir
        done

    done
}

get_folder_lst $1
loop_folder_lst $directories
