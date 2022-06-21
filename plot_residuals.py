import sys
import re
import numpy as np
import matplotlib.pyplot as plt


def get_norms(filename):
    """
    Given a file containing the output from a Crane simulation,
    extract the time steps, the Steady-State Relative Differential
    Norms, and the Residual Norms of CO2 at each time step.
    """
    time_steps = []
    co2_norms = []
    steady_state_norms = []
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if re.match('Steady-State Relative.*', line):
                x = line.split('Steady-State Relative Differential Norm: ')[1]
                steady_state_norms.append(float(x))
            elif re.match('Time Step.*', line):
                x = line.split(',')[0]
                n = x.split('Time Step ')[1]
                time_steps.append((int(n)))
            elif re.match('CO2:.*', line):
                x = line.split('CO2: ')[1]
                co2_norms.append(float(x))

    return time_steps[1:], co2_norms, steady_state_norms


def plot_norms(time_steps, co2_norms, steady_state_norms, plot_dir):

    plt.figure(1)
    plt.semilogy(time_steps, steady_state_norms, 'g.-')
    plt.xlabel('time step')
    plt.ylabel('Steady-State Relative Differential Norm')
    plt.savefig(f'{plot_dir}/steady_state_norms.png')
    plt.show()

    plt.figure(2)
    plt.semilogy(time_steps, co2_norms, 'g.-')
    plt.xlabel('time step')
    plt.ylabel('CO$_2$ Residual Norm')
    plt.savefig(f'{plot_dir}/co2_residual_norms.png')
    plt.show()


def main():
    cfg = util.load_config()
    plot_dir = cfg['plot_dir']

    # Save output to file. Make sure to run
    # Crane with "--color off" to eliminate escape characters
    # in the output file.
    crane_output_file = sys.argv[1]
    time_steps, co2_norms, steady_state_norms = get_norms(crane_output_file)


    plot_norms(time_steps, co2_norms, steady_state_norms)
if __name__ == '__main__':
    main()
