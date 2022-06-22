import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import util
import os


"""
This script is meant to be run after CRANE simulations have completed. It
traverses all temperature directories and reads the CRANE output. It
compares the starting and ending CO2 densities to determine the percent
CO2 conversion.
"""


def main():
    densities = {}
    output_dirs = glob.glob('*K')
    for output_dir in output_dirs:
        temp = int(output_dir[:-1])
        densities[temp] = pd.read_csv(output_dir + '/co2_splitting_out.csv')

    cfg = util.load_config()
    plot_dir = cfg['plot_dir']
    os.makedirs(plot_dir, exist_ok=True)

    pct_conversion = []
    for temp, df in densities.items():
        starting_co2_n = df['CO2'].iloc[0]
        ending_co2_n = df['CO2'].iloc[-1]

        converted = (starting_co2_n - ending_co2_n) / starting_co2_n
        pct_conversion.append([temp, converted])

    pct_conversion.sort(key = lambda t: t[0])
    pct_conversion = np.array(pct_conversion)

    ax = util.new_pretty_plot(
        xlabel = 'Temperature (K)',
        ylabel = '%-CO$_2$ converted',
    )
    ax.plot(
        pct_conversion[:,0],
        pct_conversion[:,1],
        'r.-',
    )
    plt.savefig(f'{plot_dir}/pct_converted.png')
    plt.show()


if __name__ == '__main__':
    main()
