import os
import numpy as np
import util

"""
This script creates one directory for every temperature in the simulation
(indicated in config.yaml). It formats a Bolsig script template and places
the resulting script in each temperature directory.

Plasma density is calculated from: [1] Berthelot, A., &amp; Bogaerts, A. (2017). Modeling of CO2 Splitting in a Microwave Plasma: How to Improve the Conversion and Energy Efficiency. Journal of Physical Chemistry C, 121.

Figure 4
"""

_BOLSIG_SCRIPT_TEMPLATE = 'CO2_PLASMA.b.template'

if __name__ == '__main__':
    # Gas Temperaturs [K]
    temps = util.load_temps_from_config()

    with open(_BOLSIG_SCRIPT_TEMPLATE, 'r') as f:
        bolsig_script_fmt = f.read()

    for T in temps:
        dirname = f'{int(T):04}K'
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        # Write Bolsig script to directory
        bolsig_script = bolsig_script_fmt.format(
            T = T,
            plasma_density = util.plasma_density(T),
            output_filename = f'CO2_plasma_rates_{dirname}.dat'
        )
        with open(dirname + '/CO2_PLASMA.b', 'w') as f:
            f.write(bolsig_script)


