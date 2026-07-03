# NACA Airfoil Sweep with NeuralFoil on UTSA ARC Cluster

Parametric aerodynamic sweep of NACA 24xx airfoils using [NeuralFoil](https://github.com/peterdsharpe/NeuralFoil) — a machine learning surrogate for XFoil. Ran on the UTSA ARC HPC cluster (Slurm, `compute1` partition).

## What This Does

Evaluates NACA 2406 through NACA 2430 (13 profiles, varying thickness 6%–30%) across angles of attack from -6° to 16° at Re = 500,000. Outputs lift (CL), drag (CD), and moment (CM) coefficients as `.npz` files.

## File Structure

```
├── run_sweep.py       # Main simulation script (accepts Slurm array task ID)
├── plot_foils.py      # Post-processing: generates lift curve + drag polar plots
├── submit_arc.sh      # Slurm batch submission script for UTSA ARC
├── requirements.txt   # Python dependencies
└── results_data/      # Output folder (generated at runtime)
```

## How to Run on UTSA ARC Cluster

### 1. Set up environment (first time only)
```bash
module load miniconda
conda create --name foil_env python=3.10 -y
conda activate foil_env
pip install neuralfoil aerosandbox numpy matplotlib
```

### 2. Clone and navigate to repo
```bash
git clone https://github.com/YOUR_USERNAME/naca-neuralfoil-arc
cd naca-neuralfoil-arc
```

### 3. Create required directories
```bash
mkdir -p logs results_data
```

### 4. Submit the job array to Slurm
```bash
sbatch submit_arc.sh
```
This fires 13 parallel tasks (`--array=0-12`), one per airfoil thickness.

### 5. Monitor progress
```bash
squeue -u oub220
tail -f logs/nf_<job_id>_0.out
```

### 6. Plot results (can run on login node or locally)
```bash
python plot_foils.py
# Saves naca_results.png to current directory
# Download to local machine:
# scp oub220@arc.utsa.edu:/work/oub220/naca-neuralfoil-arc/naca_results.png ~/Desktop/
```

## How to Run Locally (Mac/Linux)

```bash
python3 -m venv foil_local
source foil_local/bin/activate
pip install -r requirements.txt

# Run a single airfoil (task ID 3 = NACA 2412)
python run_sweep.py 3

# Run the full sweep
for id in {0..12}; do python run_sweep.py $id; done

# Plot
python plot_foils.py
```

## Notes

- NeuralFoil does not accept a Mach number argument — it handles low-speed incompressible flow only
- `plt.show()` will not work on headless cluster nodes; use `matplotlib.use('Agg')` and `savefig()` instead
- UTSA ARC requires `--partition=compute1` explicitly in the Slurm script
- The `source /etc/profile.d/modules.sh` line includes `2>/dev/null || true` to suppress errors on nodes where the path differs
