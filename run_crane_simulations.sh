#!/usr/bin/env bash

# Import logging helpers for nice colors
source ./logging.sh

###
### CHANGE THIS
###
CRANE_BIN=../../../crane-opt
###
###
###


if [ ! -f $CRANE_BIN ]; then
        log_fatal executable \"$CRANE_BIN\" not found. Set path to crane\
            executable with CRANE_BIN in run_crane_simulations.sh
fi

CRANE_SCRIPT_NAME=co2_splitting.i

for dir in *K; do
        SCRIPT_PATH=$dir/$CRANE_SCRIPT_NAME
        if [ ! -f $SCRIPT_PATH ]; then
                log_error missing \"$SCRIPT_PATH\" needed to run crane
                continue
        fi

        $CRANE_BIN -i $SCRIPT_PATH

done
