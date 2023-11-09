# ref: https://www.stackchief.com/tutorials/Bash%20Tutorial%3A%20getopts
#!/bin/bash
while getopts "ab:c:" opt; do
  case $opt in
     a)
       echo "argument -a called" >&2
       ;;
     b):
       echo "argument: "$opt called: $OPTARG
  esac
done
