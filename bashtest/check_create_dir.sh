#!/bin/bash

check_and_create_dir() {
    local dir_path=$1
    echo hexalog path: $1

    # Check if the directory path is provided
    if [ -z "$dir_path" ]; then
        echo "Please provide a directory path."
        return 1
    fi

    # Check if the directory exists
    if [ -d $dir_path ]; then
        echo "The directory '$dir_path' already exists."
    else
        # Create the directory
        mkdir -p "$dir_path"
        if [ $? -eq 0 ]; then
            echo "The directory '$dir_path' has been created."
        else
            echo "Failed to create directory '$dir_path'."
            return 2
        fi
    fi
}

check_and_create_dir $HOME/hexa_log