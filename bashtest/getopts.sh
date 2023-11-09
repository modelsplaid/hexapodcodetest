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
