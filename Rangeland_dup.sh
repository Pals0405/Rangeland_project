#!/bin/bash
#SBATCH --partition=rajagopalan,stockle,cahnrs,cahnrs_bigmem,cahnrs_gpu,kamiak
#SBATCH --requeue
#SBATCH --job-name=RangelandJob # Job Name
#SBATCH --output=R_%A_%a.out
#SBATCH --error=R_%A_%a.err
#SBATCH --time=0-05:00:00    # Wall clock time limit in Days-HH:MM:SS
#SBATCH --mem=07GB 
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
cd /home/pallavi.sharma1/Final_script_rangeland/
echo "I am Slurm job ${SLURM_JOB_ID}, array job ${SLURM_ARRAY_JOB_ID}, and array task ${SLURM_ARRAY_TASK_ID}."

srun python Reading_join_file.py  ${SLURM_ARRAY_TASK_ID}