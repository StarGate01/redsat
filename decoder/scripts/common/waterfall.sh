#!/usr/bin/env bash

# Usage: ./waterfall.sh [input_file] (extra options)

DIR=$(dirname "${BASH_SOURCE[0]}")  # get the directory name
DIR=$(realpath "${DIR}")   			# resolve its full path if need be

gnuplot -e "inputfile='$1'" -e "outfile='$1.png'" -e "width=1000" -e "height=2000" $2 $DIR/waterfall.gp
