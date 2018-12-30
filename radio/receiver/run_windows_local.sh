#!/bin/bash

BASEP=/c/Users/Christoph/Documents/GitHub/redsat
BASEP_WIN="C:\\Users\\Christoph\\Documents\\GitHub\\redsat"

export REDSAT_TLE_DIR=$BASEP/persistent-data/TLE
export REDSAT_INPUT_DIR=$BASEP/persistent-data/input
export REDSAT_INPUT_DIR_WIN="$BASEP_WIN\\persistent-data\\input"
export REDSAT_GR_DIR=$BASEP/receiver/data/gr
export REDSAT_GR_DIR_WIN="$BASEP_WIN\\receiver\\data\\gr"
export REDSAT_OS=windows
export REDSAT_GR_BIN_WIN="C:\\Program Files\\GNURadio-3.7\\bin\\run_gr.bat"
#export REDSAT_DEPS_DIR=/app/deps

./run.sh