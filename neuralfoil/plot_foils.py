import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for thickness in [6, 12, 18, 24, 30]:
    filename = f"./results_data/naca24{thickness:02d}_data.npz"
    if os.path.exists(filename):
        data = np.load(filename)
        label = f"NACA 24{thickness:02d}"
        ax1.plot(data['alpha'], data['cl'], label=label, linewidth=2)
        ax2.plot(data['cd'], data['cl'], label=label, linewidth=2)

ax1.set_xlabel('Angle of Attack (deg)')
ax1.set_ylabel('Lift Coefficient (CL)')
ax1.set_title('Lift Curves')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

ax2.set_xlabel('Drag Coefficient (CD)')
ax2.set_ylabel('Lift Coefficient (CL)')
ax2.set_title('Drag Polars')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig('naca_results.png', dpi=300)
print("Saved to naca_results.png")
