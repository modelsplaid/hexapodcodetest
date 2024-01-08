
dir="."

# Check if there are any .txt files in the directory
if ls "$dir"/*.txt 1> /dev/null 2>&1; then
    # If .txt files exist, remove them
    echo "Removing .txt files in $dir..."
    rm "$dir"/*.txt

    echo "Files removed."
fi

file_name_by_cur_time() {
    file_nam=$1".txt"

    current_time=$(date +"%Y%m%d-%H-%M-%S")
    file_name=$current_time-$file_nam
    echo $file_name
}

#ls > $(file_name_by_cur_time hexa_cleaner)
touch $(file_name_by_cur_time "hexa_cleaner")
