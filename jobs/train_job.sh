#!/bin/bash
#SBATCH --job-name=train-vit     # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=4        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=4G         # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=36:00:00          # total run time limit (HH:MM:SS)
#SBATCH --nodelist=selab2

module purge

source ~/miniconda3/etc/profile.d/conda.sh

conda activate fsd

pip install .

python src/train.py -c configs/train/double_head_resnet.yml
