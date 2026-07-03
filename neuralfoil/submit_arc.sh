#!/bin/bash
#SBATCH --job-name=naca_neuralfoil
#SBATCH --partition=compute1
#SBATCH --output=logs/nf_%A_%a.out
#SBATCH --error=logs/nf_%A_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:20:00
#SBATCH --mem=4G
#SBATCH --array=0-12
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=abhishek.das@my.utsa.edu

source /etc/profile.d/modules.sh 2>/dev/null || true
module load miniconda 2>/dev/null || true
source activate foil_env

python run_sweep.py $SLURM_ARRAY_TASK_ID
