#!/usr/bin/env bash

PROJECT_NAME="Rezazadeh_Mikhail_Module_3_Project"
CODE_DIR="${PROJECT_NAME}_Code"
DIST_DIR=dist
DIST_NAME="${CODE_DIR}.zip"

mkdir -p $DIST_DIR/$CODE_DIR

# Config files + setup
cp README.md $DIST_DIR/$CODE_DIR
cp requirements.txt $DIST_DIR/$CODE_DIR
cp config.yaml $DIST_DIR/$CODE_DIR

# copy bash scripts + helper files
cp clean.sh $DIST_DIR/$CODE_DIR
cp run_bolsigminus.sh $DIST_DIR/$CODE_DIR
cp run_crane_simulations.sh $DIST_DIR/$CODE_DIR
cp logging.sh $DIST_DIR/$CODE_DIR

# copy Bolsig script template + file containing cross section data from LxCat
cp CO2_PLASMA.b.template $DIST_DIR/$CODE_DIR
cp co2_splitting_cross_sections.dat $DIST_DIR/$CODE_DIR

# copy Python files required to setup simulations
cp build_bolsig_scripts.py $DIST_DIR/$CODE_DIR
cp build_crane_input_files.py $DIST_DIR/$CODE_DIR
cp parse_bolsig_output.py $DIST_DIR/$CODE_DIR
cp util.py $DIST_DIR/$CODE_DIR

# copy CRANE template
cp co2_splitting.i.template	$DIST_DIR/$CODE_DIR

# Post-processing of data
cp plot_co2_splitting_rates.py $DIST_DIR/$CODE_DIR
cp plot_residuals.py $DIST_DIR/$CODE_DIR

# Make archive
cd $DIST_DIR
zip -r $DIST_NAME $CODE_DIR
cd ..

