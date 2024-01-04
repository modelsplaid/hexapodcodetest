#!/bin/bash

# Check if an argument (video file) is given
# """
# The line if [ "$#" -ne 1 ]; then is a condition used in Bash scripting, and it's checking the number of arguments passed to the script:
# if: This introduces a conditional statement.
# [ ... ]: This is a test command, also known as a conditional expression.
# "$#": This is a special parameter in Bash that represents the number of positional parameters (arguments) passed to the script.
# -ne: This stands for "not equal" in arithmetic comparison.
# 1: This is the number being compared against.
# """

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <video_file>"
    exit 1
fi

input_video=$1
output_video="${input_video%.*}_360p.${input_video##*.}"

# Command to compress and resize the video
#ffmpeg -i "$input_video" -vf "scale=16:10" -b:v 1k -b:a 1k -c:a copy "$output_video"
ffmpeg -i "$input_video" -vf "scale=16:10" -b:v 1k -b:a 64k "$output_video"

echo "Compression complete. Output file: $output_video"
