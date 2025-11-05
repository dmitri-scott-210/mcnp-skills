#!/bin/bash -l
#PBS -A FUSIONSDR
#PBS -l select=64:mpiprocs=2:ncpus=64
#PBS -l walltime=04:00:00
#PBS -N MSRE-CAD
#PBS -j oe
#PBS -m abe
#PBS -M promano@anl.gov

cd $PBS_O_WORKDIR

conda activate py311
export OPENMC_CROSS_SECTIONS=$(pwd)/../openmc_csg/cross_sections_80.xml
export OMP_SCHEDULE=dynamic,1

mpiexec ~/openmc/build/bin/openmc msre_cad.xml
