#!/bin/bash
#SBATCH --partition=rajagopalan,stockle,cahnrs,cahnrs_bigmem,cahnrs_gpu,kamiak
#SBATCH --requeue
#SBATCH --job-name=RangelandFinalJob # Job Name
#SBATCH --output=R_%A_%a.out
#SBATCH --error=R_%A_%a.err
#SBATCH --time=4-00:00:00    # Wall clock time limit in Days-HH:MM:SS
#SBATCH --mem=300GB 
#SBATCH --nodes=1            # Node count required for the job
#SBATCH --ntasks-per-node=1  # Number of tasks to be launched per Node
#SBATCH --ntasks=1           # Number of tasks per array job
#SBATCH --cpus-per-task=1    # Number of threads per task (OMP threads)


echo
echo "--- We are now in $PWD, running an python script ..."
echo

# Load python on compute node
module load python
cd /home/pallavi.sharma1/Rangeland_scripts/

srun python Reading_monthly_files.py 
