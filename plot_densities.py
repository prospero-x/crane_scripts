import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

filename = sys.argv[1]
data = pd.read_csv(filename)

fig, ax = plt.subplots()
time = data['time'] * 1e3
ax.semilogy(time, data['CO2'], 'k', label='CO2')
ax.set_xlabel('Time (ms)', fontsize=20)
ax.set_ylabel('Density (cm$^{-3}$)', fontsize=20)
ax.tick_params(axis='both', labelsize=15)
ax.legend(fontsize=10, loc='best', ncol=5)
#ax.set_ylim([1e3, 1e14])
plt.show()
