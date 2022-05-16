#!/bin/bash
#SBATCH --partition=rajagopalan,stockle,cahnrs,cahnrs_bigmem,cahnrs_gpu,kamiak
#SBATCH --requeue
#SBATCH --job-name=RangelandJob # Job Name
#SBATCH --output=R_%A_%a.out
#SBATCH --error=R_%A_%a.err
#SBATCH --time=0-03:00:00    # Wall clock time limit in Days-HH:MM:SS
#SBATCH --mem=03GB 
#SBATCH --nodes=1            # Node count required for the job
#SBATCH --ntasks-per-node=1  # Number of tasks to be launched per Node
#SBATCH --ntasks=1           # Number of tasks per array job
#SBATCH --cpus-per-task=1    # Number of threads per task (OMP threads)
#SBATCH --array=0-1


echo
echo "--- We are now in $PWD, running an python script ..."
echo

# Load python on compute node
module load python
cd /home/pallavi.sharma1/Rangeland_scripts/
echo "I am Slurm job ${SLURM_JOB_ID}, array job ${SLURM_ARRAY_JOB_ID}, and array task ${SLURM_ARRAY_TASK_ID}."

srun python reading_gridmet_data_script.py ${SLURM_ARRAY_TASK_ID}
