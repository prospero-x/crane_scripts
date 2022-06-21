
## Requirements
1. [Crane](https://github.com/lcpp-org/crane) 
2. [bolsigminus](http://www.bolsig.laplace.univ-tlse.fr/download.html)

## Setup
`pip install -r requirements.txt`

## Configure Simulations
Modify the Temperature parameterizations in `config.yaml`. `N` is the number
of crane simulations that will be run.

## Setup Crane Simulations
1. `$python build_bolsig_scripts.py` this will create one directory for
    every temperature in the simulation (configure in `config.yaml`)
2. Set path to `bolsigminus` binary in `run_bolsigminus.sh`
3. Run `$./run_bolsigminus.sh` This runs the Bolztmann solver to create rates
for every electron impact reaction
4. Run `$python parse_bolsig_output.py` This parses the single output file from the Boltzmann solver and places the rate coefficients for each electron impact reaction in side each temperature folder in `electron_impact_reactions` e.g. `300K/electron_impact_reactions/`
5. Run `$python build_crane_input_files.py` This places a Crane input
file in each temperature directory, configuring it with the appropriate
initial CO2 density according to the temperature.

## Run Crane Simulations
1. Set path to `crane-opt` executable in `run_crane_simulations.sh`
2. Run `$./run_crane_simulations.sh` This runs crane for each temperature. Output is saved to each temperature directory in a file named `co2_splitting_out.csv`

## Post-processing
To plot the rate of CO2 dissociation vs Gas Temp, run `python plot_co2_splitting_densities.py`

To view residuals of a **single** crane simulation, run:
1. Run `$<CRANE_OPT> --color off -i <TEMP_DIR>/co2_splitting.i &>crane_output.txt`, where `<CRANE_OPT>` is the path to the already-installed crane executable and `<TEMP_DIR>` is the directory created by the above process.
2. Run `$python plot_residuals.py crane_output.txt`



# File Overview
- `build_bolsig_scripts.py` This creates one directory for every gas temperature for the simulations. Temperatures are configured in `config.yaml`. It formats a template bolsig script and places it in each temperature directory
- `build_crane_input_files.py` creates one directory for every gas temperature for the simulations. Temperatures are configures in `config.yaml`. It formats a template CRANE input file and places it in each temperature directory.
- `CO2_PLASMA.b.template` Bolsig script template
- `co2_splitting.i.template` CRANE input file template
- `co2_splitting_cross_sections.dat` electron impact cross sections from LxCat
- `config.yaml` Config for defining min/max gas temp and number of steps
- `logging.sh` contains helper Bash functions for better logging
- `parse_bolsig_output.py` Parses output of Bolsig+ into separate files, one for each
electron impact reaction. For each temperature directory, it creates a subdirectory `electron_impact_reactions` into which each file containing rate coefficients is placed
- `plot_co2_splitting_rates.py` iterates across all temperature directories and compares starting and ending CO2 densiteis. Post-processing, meant for after all CRANE simulations are complete.
- `plot_residuals.py` takes a text file containing output from a **single** CRANE simulation and plots the CO2 residuals for each time step
- `requirements.txt` dependencies for pip
- `run_bolsigminus.sh` Runs Bolsig+ (bolsigminus) for every temperature directory. Bolsig scripts must already exist
- `run_crane_simulations.sh` Runs CRANE for every temperature directory. CRANE input files must already exist
- `util.py` helper functions for Python scripts
