import os
import numpy as np
import util

"""
This script creates one directory for every temperature indicated in the
config file (config.yaml) (if it doesn't already exist) and formats a
CRANE input file from a template.

The initial gas density is calculated using the Ideal Gas Law, assuming
pressure is 100 mBar.

The initial electron density is estimated by looking at Figure 4 of:
    [1] Berthelot, A., &amp; Bogaerts, A. (2017). Modeling of CO2 Splitting in a Microwave Plasma: How to Improve the Conversion and Energy Efficiency. Journal of Physical Chemistry, C. 121.
"""

_CRANE_INPUT_FILE_TEMPLATE = 'co2_splitting.i.template'


def format_crane_script(crane_script_fmt, kv):
    """
    Crane contains lots of explicit '{' and '}' so I'm just doing
    a brute-force explicit replace of keys with values.
    """
    for k, v in kv.items():
        crane_script_fmt = crane_script_fmt.replace(k, v)

    return crane_script_fmt

if __name__ == '__main__':
    # Gas Temperaturs [K]
    temps = util.load_temps_from_config()

    with open(_CRANE_INPUT_FILE_TEMPLATE, 'r') as f:
        crane_input_file_fmt = f.read()

    for T in temps:
        dirname = f'{int(T):04}K'
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        # Write Crane input file to directory
        crane_input_file = format_crane_script(
            crane_input_file_fmt,
            {
                'GAS_TEMPERATURE': f'{int(T)}',
                'ELECTRON_IMPACT_RATES_DIR': dirname + '/electron_impact_rates',
                'ELECTRON_DENSITY': f'{util.plasma_density(T):e}',
                'CO2_DENSITY': f'{util.co2_density(T):e}',
            }
        )

        crane_input_fname = f'{dirname}/co2_splitting.i'
        with open(crane_input_fname, 'w') as f:
            f.write(crane_input_file)
        print(f'wrote CRANE input file {crane_input_fname}')


