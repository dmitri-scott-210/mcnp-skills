import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Plot customizations
mpl.rcParams['axes.axisbelow'] = True
mpl.rcParams['font.size'] = 12.0
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['savefig.bbox'] = 'tight'

threads = np.array([1, 2, 4, 8, 16, 32, 64])
csg_inactive = np.array([
    1535.79, 3069.91, 5950.28, 11724.7, 23096.6, 45585.5, 86869.8
])
csg_active = np.array([
    1093.47, 2111.51, 3831.45, 7438.84, 14483.7, 28298.1, 53144.4
])

cad_nodd_inactive = np.array([
    55.3626, 76.9338, 80.7354, 93.0245, 99.3696, 99.7712, 101.864
])
cad_nodd_active = np.array([
    52.8279, 73.5609, 77.2614, 88.8872, 95.1981, 95.6719, 98.0266
])

cad_dd_inactive = np.array([
    927.071, 1796.06, 3015.56, 6069.9, 12254.2, 22763.6, 38942.8
])
cad_dd_active = np.array([
    763.178, 1456.13, 2394.19, 4753.3, 9353.36, 17363.5, 29938.2
])

fig, ax = plt.subplots()
ax.loglog(threads, csg_inactive, color='C0', marker='o', ls='-', label='CSG, inactive')
ax.loglog(threads, csg_active, color='C0', marker='o', ls='--', label='CSG, active')
ax.loglog(threads, cad_nodd_inactive, color='C1', marker='x', ls='-', label='CAD (MOAB), inactive')
ax.loglog(threads, cad_nodd_active, color='C1', marker='x', ls='--', label='CAD (MOAB), active')
ax.loglog(threads, cad_dd_inactive, color='C2', marker='s', ls='-', label='CAD (Embree), inactive')
ax.loglog(threads, cad_dd_active, color='C2', marker='s', ls='--', label='CAD (Embree), active')
ax.set_xlabel('Threads')
ax.set_ylabel('Calculate rate [particles/sec]')
ax.set_xticks(threads, labels=threads)
ax.tick_params(axis='x', which='minor', bottom=False)
ax.grid(which='major', axis='x')
ax.grid(which='both', axis='y')
ax.legend(loc='lower right', bbox_to_anchor=(1.0, 0.2), framealpha=1.0, fontsize=10)
fig.savefig('thread_scaling.pdf')

fig, ax = plt.subplots()
ax.semilogx(threads, csg_inactive / (threads * csg_inactive[0]), color='C0', marker='o', ls='-', label='CSG, inactive')
ax.semilogx(threads, csg_active / (threads * csg_active[0]), color='C0', marker='o', ls='--', label='CSG, active')
ax.semilogx(threads, cad_nodd_inactive / (threads * cad_nodd_inactive[0]), color='C1', marker='x', ls='-', label='CAD (MOAB), inactive')
ax.semilogx(threads, cad_nodd_active / (threads * cad_nodd_active[0]), color='C1', marker='x', ls='--', label='CAD (MOAB), active')
ax.semilogx(threads, cad_dd_inactive / (threads * cad_dd_inactive[0]), color='C2', marker='s', ls='-', label='CAD (Embree), inactive')
ax.semilogx(threads, cad_dd_active / (threads * cad_dd_active[0]), color='C2', marker='s', ls='--', label='CAD (Embree), active')
ax.set_xlabel('Threads')
ax.set_ylabel('Parallel efficiency')
ax.set_ylim(ymin=0.0)
ax.set_xticks(threads, labels=threads)
ax.tick_params(axis='x', which='minor', bottom=False)
ax.grid(which='major', axis='x')
ax.grid(which='both', axis='y')
ax.legend()
fig.savefig('parallel_efficiency.pdf')

