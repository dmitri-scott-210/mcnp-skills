#!/bin/bash -l
#PBS -A FUSIONSDR
#PBS -l select=1:mpiprocs=2:ncpus=64
#PBS -l walltime=04:00:00
#PBS -N MSRE-performance
#PBS -j oe
#PBS -m abe
#PBS -M promano@anl.gov

cd $PBS_O_WORKDIR

conda activate py311
export OPENMC_CROSS_SECTIONS=$(pwd)/../openmc_csg/cross_sections_80.xml
export OMP_SCHEDULE=dynamic,1

# CSG thread scaling, best of 3 for each run
for threads in 01 02 04 08 16 32 64; do
    for i in 1 2 3; do
	echo Running CSG with ${threads} threads, run $i...
	mpiexec -n 1 ~/openmc/build/bin/openmc -s ${threads} msre_csg_endf80_tallies.xml > csg_${threads}_run${i}.stdout
	mv statepoint.40.h5 csg_${threads}_run${i}.h5
    done
done

# CAD thread scaling (no DD), best of 3 for each run
for threads in 01 02 04 08 16 32 64; do
    for i in 1 2 3; do
	echo Running CAD no DD with ${threads} threads, run $i...
	mpiexec -n 1 ~/openmc/build_moab55/bin/openmc -s ${threads} msre_cad_endf80_tallies.xml > cad_nodd_${threads}_run${i}.stdout
	mv statepoint.40.h5 cad_nodd_${threads}_run${i}.h5
    done
done

# CAD thread scaling (DD), best of 3 for each run
for threads in 01 02 04 08 16 32 64; do
    for i in 1 2 3; do
	echo Running CAD DD with ${threads} threads, run $i...
	mpiexec -n 1 ~/openmc/build_moab55_dd/bin/openmc -s ${threads} msre_cad_endf80_tallies.xml > cad_dd_${threads}_run${i}.stdout
	mv statepoint.40.h5 cad_dd_${threads}_run${i}.h5
    done
done
