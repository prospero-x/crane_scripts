import yaml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, cm, colors
import sys

CONFIG_FILE = 'config.yaml'

kB = 1.381e-23


class ConfigException(Exception):
    pass


def validate_config(cfg):
    """
    Make sure the config yaml contains all expected keys.
    """
    _expected_keys = [
        'min_temp',
        'max_temp',
        'N'
    ]

    for key in _expected_keys:
        if key not in cfg:
            raise ConfigException(
                'expected key "%s" not found in "%s"' %(key, CONFIG_FILE),
            )

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        cfg = yaml.load(f, Loader = yaml.BaseLoader)

    validate_config(cfg)
    return cfg


def load_temps_from_config():
    """
    Return a numpy array of Simulation temperatures (in Kelvin) based on
    the configured values in config.yaml
    """
    with open(CONFIG_FILE, 'r') as f:
        cfg = yaml.load(f, Loader = yaml.BaseLoader)

    validate_config(cfg)

    return np.linspace(
        float(cfg['min_temp']),
        float(cfg['max_temp']),
        int(cfg['N']),
    )


def linearly_interpolate(Tgas, electron_densities):
    known_temps = sorted(electron_densities.keys())
    t = known_temps[0]

    n = 0
    for n in range(len(known_temps) - 1):
        if t <= Tgas:
            break
        t = known_temps[n]

    lower_ne = electron_densities[t]
    upper_ne = electron_densities[known_temps[n+1]]
    next_Tgas = known_temps[n+1]
    pct_between = (Tgas - t) / (next_Tgas -t)

    ne = pct_between * (upper_ne - lower_ne)  + lower_ne
    return ne


def co2_density(Tgas):
    """
    Calculate the density of CO2 at 100mBar with the Ideal Gas Law
    """
    # 1 m^3
    V = 1

    # 100 mBar -> Pascals
    P = 0.1 * 1e6

    N = P * V/ (kB * Tgas)
    return N

def plasma_density(Tgas):
    """
    Calculate gas density by a rough approximation of this paper:

        Modeling of CO2 Splitting in a Microwave Plasma: How to Improve
        the Conversion and Energy Efficiency, Berthelot, Bogaerts, 2017

    Figure 4 d) (Pmax *5, 100 mBar)
    """

    # Gas Temperature [K] -> Electron Density m^-3
    _electron_densities = {
        300: 2E14,
        600: 1.5E17,
        900: 3E17,
        1200:4E17,
        1500:5E17,
        1800:5.5E17,
        2100:6E17,
        2400:7E17,
        2700:8E17,
        3000:9E17,
    }


    return linearly_interpolate(Tgas, _electron_densities)


BASH_RED='\033[1;31m'
BASH_LIGHT_RED='\033[0;31m'
BASH_YELLOW='\033[0;33m'
BASH_GREEN='\033[0;32m'
BASH_BLUE='\033[0;34m'
BASH_LIGHT_BLUE='\033[2;36m'
BASH_GREY='\033[0;37m'
BASH_NOCOLOR='\033[0m'

def print_red(m=''):
    print(f'{BASH_RED}{m}{BASH_NOCOLOR}')

def print_green(m=''):
    print(f'{BASH_GREEN}{m}{BASH_NOCOLOR}')

def print_yellow(m=''):
    print(f'{BASH_YELLOW}{m}{BASH_NOCOLOR}')


class PrettyPlot:


    def __init__(self, ax, linewidth, markersize):
        self.ax = ax
        self.linewidth = linewidth
        self.markersize = markersize

    def set_kwargs(self, kwargs):
        kwargs['linewidth'] = kwargs.get('linewidth', self.linewidth)
        kwargs['markersize'] = kwargs.get('markersize', self.markersize)


    def plot(self, *args, **kwargs):
        self.set_kwargs(kwargs)
        self.ax.plot(*args, **kwargs)

    def semilogy(self, *args, **kwargs):
        self.set_kwargs(kwargs)
        self.ax.semilogy(*args, **kwargs)

    def semilogx(self, *args, **kwargs):
        self.set_kwargs(kwargs)
        self.ax.semilogx(*args, **kwargs)

    def loglog(self, *args, **kwargs):
        self.set_kwargs(kwargs)
        self.ax.loglog(*args, **kwargs)


def new_pretty_plot(xlabel = '', ylabel = '', title = '',
                fontsize = 24,
                figsize = (14, 12),
                linewidth = 3,
                markersize = 20):

    fig = plt.figure(figsize = figsize)
    ax = plt.axes()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
    ax.yaxis.offsetText.set_fontsize(fontsize)
    ax.xaxis.offsetText.set_fontsize(fontsize)

    ax.set_ylabel(ylabel, fontsize = fontsize)
    ax.set_xlabel(xlabel, fontsize = fontsize)
    ax.set_title(title, fontsize = fontsize)
    return PrettyPlot(ax, linewidth, markersize)


def new_panel_plot(nrows, ncols,
                xlabels = None, ylabels = None, titles = None,
                fontsize = 24,
                linewidth = 3,
                markersize = 20):

    if nrows == 1:
        figsize = (24, 10)
    elif nrows == 2:
        figsize = (24, 20)

    _, axs = plt.subplots(nrows, ncols, figsize = figsize)


    xlabels = xlabels or ['']*nrows*ncols
    ylabels = ylabels or ['']*nrows*ncols
    titles = titles or ['']*nrows*ncols

    if nrows > 1:
        for i in range(nrows):
            for j in range(ncols):
                axs[i][j].tick_params(
                    axis = 'both', which = 'major', labelsize = fontsize)
                axs[i][j].tick_params(
                    axis = 'both', which = 'minor', labelsize = fontsize)
                axs[i][j].xaxis.offsetText.set_fontsize(fontsize)
                axs[i][j].yaxis.offsetText.set_fontsize(fontsize)

                input_idx = i*(ncols-1) + j
                axs[i][j].set_xlabel(xlabels[input_idx], fontsize = fontsize)
                axs[i][j].set_ylabel(ylabels[input_idx], fontsize = fontsize)
                axs[i][j].set_title(titles[input_idx], fontsize = fontsize)

                axs[i][j] = PrettyPlot(axs[i][j])
    else:
        for j in range(ncols):
            axs[j].tick_params(
                axis = 'both', which = 'major', labelsize = fontsize)
            axs[j].tick_params(
                axis = 'both', which = 'minor', labelsize = fontsize)
            axs[j].xaxis.offsetText.set_fontsize(fontsize)
            axs[j].yaxis.offsetText.set_fontsize(fontsize)
            axs[j].set_xlabel(xlabels[j], fontsize = fontsize)
            axs[j].set_ylabel(ylabels[j], fontsize = fontsize)
            axs[j].set_title(titles[j], fontsize = fontsize)
            axs[j] = PrettyPlot(axs[j], linewidth, markersize)

    return axs




def add_legend(ax, fontsize = 24):
    ax.legend(prop = dict(size=fontsize))

def add_legends(axs, nrows, ncols, fontsize = 24):
    for i in range(nrows):
        for j in range(ncols):
            if nrows > 1:
                axs[i][j].legend(prop = dict(size = fontsize))
            else:
                axs[j].legend(prop = dict(size = fontsize))


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def plt_show(ax):
    add_legend(ax)
    plt.show()
