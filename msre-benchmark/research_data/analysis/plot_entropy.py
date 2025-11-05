import openmc
import matplotlib.pyplot as plt
import matplotlib as mpl

# Plot customizations
mpl.rcParams['axes.axisbelow'] = True
mpl.rcParams['font.size'] = 12.0
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['savefig.bbox'] = 'tight'



with openmc.StatePoint('../models/openmc_csg/results/entropy_results.h5') as sp:
    entropy = sp.entropy
mean = entropy[100:].mean()

fig, ax = plt.subplots()
ax.plot(entropy - mean)
ax.set_xlim(0, 200)
ax.set_ylim(-0.05, 0.05)
ax.grid(True)
ax.set_xlabel('Batch')
ax.set_ylabel('Normalized Entropy')
fig.savefig('entropy.pdf')
