#!/bin/bash

==================================================================
INFO
==================================================================

# Title

#README for running FSL PALM 


==================================================================
A) PREP WORK
==================================================================


## SOME PREP WORK
------------------------------------------------------------------

# Extract subjectkeys from all participants and save into a text file
for f in /Users/Lara/Documents/ABCD/Myelin_analysis/Random1001/Myelin_maps/NDAR*; do echo $f | cut -d. -f1  | cut -d/ -f8; done > Random_Subjectkeys.txt 

# Extract paths to all participants, save into a text file and add ‘-cifti’ in the beginning of each path and ‘-column 1’ in the end
for f in /Users/Lara/Documents/ABCD/Myelin_analysis/Myelin_maps_Random1001/NDAR*; do echo $f; done > Random_paths.txt 
awk '{print "-cifti " $0}' Random_paths.txt > Random1001_cifti_paths.txt
awk '{print $0 " -column 1"}' Random1001_cifti_paths.txt > Random_cifti_column_paths.txt


# Run -cifti-separate to get input files needed for PALM
wb_command -cifti-separate Random/PALM_input/Random.dscalar.nii  COLUMN -metric CORTEX_LEFT Random_L.func.gii -metric CORTEX_RIGHT Random_MMM_R.func.gii


## CREATE AVERAGE SURFACE AREAS
------------------------------------------------------------------

# Average areas (across all subjects’ surfaces) are optional but recommended
# Below code is following “Example 10” on https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PALM/Examples

# FOR LEFT HEMISPHERE

# Create variable containing all individual subject keys (LH)
SUBJECT_KEYS_L=$(for f in Midthickness_surfaces_Random1001/*.L.*surf.gii; do echo $f | cut -d/ -f8 | cut -d. -f1; done)
# Make sure variable contains right amount of subjects
for f in $SUBJECT_KEYS_L; do echo $f; done | wc -l


for file in ${SUBJECT_KEYS_L}; do 
	wb_command -surface-vertex-areas Midthickness_surfaces_Random/${file}.L.midthickness.32k_fs_LR.surf.gii Average_areas_Random/${file}.L.midthick.va.shape.gii;
done

# Merge all average areas into one file
L_MERGELIST=“”
for subj in ${SUBJECT_KEYS_L} ; do
	L_MERGELIST=“${L_MERGELIST} -metric ${subj}.L.midthick.va.shape.gii”; done

cd Average_areas_Random
wb_command -metric-merge L.midthick.va.func.gii ${L_MERGELIST}
wb_command -metric-reduce L.midthick.va.func.gii MEAN L_area.func.gii


# FOR RIGHT HEMISPHERE 

# Create variable containing all individual subject keys (LH)
SUBJECT_KEYS_R=$(for f in Midthickness_surfaces_Random/*.R.*surf.gii; do echo $f | cut -d/ -f8 | cut -d. -f1; done)
# Make sure variable contains right amount of subjects
for f in $SUBJECT_KEYS_R; do echo $f; done | wc -l


for file in ${SUBJECT_KEYS_R}; do 
	wb_command -surface-vertex-areas Midthickness_surfaces_Random/${file}.R.midthickness.32k_fs_LR.surf.gii Average_areas_Random/${file}.R.midthick.va.shape.gii;
done


# Merge all average areas into one file
R_MERGELIST=“”
for subj in ${SUBJECT_KEYS_R} ; do
	R_MERGELIST=“${R_MERGELIST} -metric ${subj}.R.midthick.va.shape.gii”; done

cd Average_areas_Random
wb_command -metric-merge R.midthick.va.func.gii ${R_MERGELIST}
wb_command -metric-reduce R.midthick.va.func.gii MEAN R_area.func.gii


==================================================================
B) RUN PALM
==================================================================


# PALM for both hemispheres with ORR scores
./palm -i Random_L.func.gii -i Random_R.func.gii -d Random_ORR.mat -t Random.con -o Random_ORR -s midthickness_average_L.surf.gii L_area.func.gii -s midthickness_average_R.surf.gii R_area.func.gii -eb EBs.csv -T -tfce2D -logp -corrmod -corrcon

==================================================================
A) POST PALM
==================================================================

# FOR ORR
# For contrast 1
wb_command -cifti-create-dense-from-template /Random/PALM_input/Random.dscalar.nii Random1_ORR_tfce_tstat_mfwep_c1.dscalar.nii -metric CORTEX_LEFT Random_ORR_tfce_tstat_mfwep_m1_c1.gii -metric CORTEX_RIGHT Random_ORR_tfce_tstat_mfwep_m2_c1.gii

# For contrast 2
wb_command -cifti-create-dense-from-template /Random/PALM_input/Random.dscalar.nii Random1_ORR_tfce_tstat_mfwep_c2.dscalar.nii -metric CORTEX_LEFT Random_ORR_tfce_tstat_mfwep_m1_c2.gii -metric CORTEX_RIGHT Random_ORR_tfce_tstat_mfwep_m2_c2.gii