#!/usr/bin/env bash

# Import logging helpers for nice colors
source ./logging.sh

####
### CHANGE THIS
####
BOLSIGMINUS_BIN=./bolsigminus
###
###
###

if [ ! -f $BOLSIGMINUS_BIN ]; then
        log_fatal executable \"$BOLSIGMINUS_BIN\" not found. Set path to bolsigminus\
            executable with BOLSIGMINUS_BIN in run_bolsigminus.sh
fi

BOLSIGMINUS_SCRIPT_NAME=CO2_PLASMA.b

for dir in *K; do
        SCRIPT_PATH=$dir/$BOLSIGMINUS_SCRIPT_NAME
        if [ ! -f $SCRIPT_PATH ]; then
                log_error missing \"$SCRIPT_PATH\" needed to run bolsigminus
                continue
        fi

        $BOLSIGMINUS_BIN $SCRIPT_PATH

        # Bolsigminus is finicky and doesn't let you specify a sub directory
        # as an output file. So we let it save the output to the current directory
        # and then copy into the subdir
        output_file=CO2_plasma_rates_$dir.dat
        mv $output_file $dir
done
