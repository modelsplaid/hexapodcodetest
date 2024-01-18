#!/bin/bash

# Check if two arguments are given (two directory paths)
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 directory1 directory2"
    exit 1
fi

dir1=$1
dir2=$2

# Check if both arguments are directories
if [ ! -d "$dir1" ] || [ ! -d "$dir2" ]; then
    echo "Both arguments must be directories."
    exit 1
fi


# Find files in both directories (only base names)
files1=$(find "$dir1" -maxdepth 1  -not -name ".*" -exec basename {} \;)
files2=$(find "$dir2" -maxdepth 1  -not -name ".*"  -exec basename {} \;)


# Find duplicates
duplicates=$(echo "$files1"$'\n'"$files2" | sort | uniq -d)

if [ -z "$duplicates" ]; then
    #echo "No duplicate file names found between $dir1 and $dir2."
    pass=''
else
    echo "Duplicate file names found:"
    #echo "$duplicates"
    for str_prc in ${duplicates}; do
        echo ${dir1}/"$str_prc"":" 
        du -h -d 0 ${dir1}/"$str_prc" 
        du -h -d 0 ${dir2}/"$str_prc"
    done

    echo "Choose which to delete (1/2), or no action (n) ?:"
    read user_input

    if [ $user_input == 1 ]; then
        echo Delete first file
        rm -rf ${dir1}/"$str_prc"

    elif [ $user_input == 2 ]; then
        echo Delete second file
        rm -rf ${dir2}/"$str_prc"
    else
        echo No action.
    fi

fi










# """
# Chat gpt4 

# User
# write a bash scripts, which can detect name repetitions between two directories


# User
# what value can i choose for parameter -type and -exec for the command find?


# In the find command in Unix and Unix-like operating systems, the -type and -exec parameters are quite versatile and can be used in various ways:

# -type Parameter:
# This parameter is used to specify the type of files that you want to search for. Common values for this parameter include:

# f: Regular file
# d: Directory
# l: Symbolic link
# c: Character devices
# b: Block devices
# s: Socket
# p: Named pipe (FIFO)
# Example: find /path/to/search -type f searches for regular files.

# -exec Parameter:
# The -exec parameter allows you to execute a command on each file found by find. This is a powerful feature as it lets you process or manipulate the matching files directly. The syntax is -exec command {} \;, where {} is replaced by the name of the current file.

# Examples:

# find /path/to/search -type f -exec ls -l {} \; will list details of each file found.
# find /path/to/search -type f -exec chmod 755 {} \; will change the permissions of each file found to 755.
# The command specified with -exec is executed once for each matching file. If you want to run a single command for all matched files, you can use -exec command {} +. This will replace {} with as many pathnames as possible for each invocation of the command.

# Remember, when using the -exec option, it's essential to end the command with either \; or +, to indicate the end of the command that find should execute. The backslash \ is used to escape the semicolon ; from shell interpretation, as ; is a special character in most shell environments.
# """
