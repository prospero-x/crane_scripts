import yaml
import numpy as np

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
