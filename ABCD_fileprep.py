#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:06:58 2021

@author: Lara
"""

########
##
# Unzip ABCD structural data and simplify folder structure
## 
########

####_________________
# Import modules     \_______________________________________________________________
####

import tarfile  
import os 
import glob
import shutil
import gzip
import pandas as pd


####_________________
# Unzip files.       \_______________________________________________________________
####

# Unzip baseline T1w images     
path = '/fmriresults01/*baseline*T1*.tgz'



fil = glob.glob(path)

for f in fil:
    print(f)  
    # open file 
    file = tarfile.open(f) 
    
    # Take subject ID and make it the name of the folder that the data is extracted into 
    name = f.split('/')[-1].split('_')[0]
    new_folder = os.path.join('./Extracted_data/Baseline/T1w', name)
    file.extractall(new_folder)
    file.close() 
    
    
# Unzip baseline T2w images     
path = '/fmriresults01/*baseline*T2*.tgz'

fil = glob.glob(path)

for f in fil:
    print(f)  
    # open file 
    file = tarfile.open(f) 
    
    # Take subject ID and make it the name of the folder that the data is extracted into 
    name = f.split('/')[-1].split('_')[0]
    new_folder = os.path.join('./Extracted_data/Baseline/T2w', name)
    file.extractall(new_folder)
    file.close()    
    
    
# Unzip 2 year follow-up T1w images 
path = '/fmriresults01/*Follow*T1*.tgz'

fil = glob.glob(path)

for f in fil:
    print(f)  
    # open file 
    file = tarfile.open(f) 
    
    # Take subject ID and make it the name of the folder that the data is extracted into 
    name = f.split('/')[-1].split('_')[0]
    new_folder = os.path.join('./Extracted_data/FollowUp/T1w', name)
    file.extractall(new_folder)
    file.close()
    
    
# Unzip 2 year follow-up T2w images 
path = '/fmriresults01/*Follow*T2*.tgz'

fil = glob.glob(path)

for f in fil:
    print(f)  
    # open file 
    file = tarfile.open(f) 
    
    # Take subject ID and make it the name of the folder that the data is extracted into 
    name = f.split('/')[-1].split('_')[0]
    new_folder = os.path.join('./Extracted_data/FollowUp/T2w', name)
    file.extractall(new_folder)
    file.close()


####_________________________
# Simplify folder structure  \_______________________________________________________________
####


path = '/Extracted_data/*/*/ND*/sub-ND*/ses-*/anat/*.*'
fil = glob.glob(path)

# Move image files up three levels in folder structure so they end up directly in subject-specific folder
for f in fil:
    print(f)   
    name = f.split('/')[1:7]
    destination_dir = '/' + os.path.join(*name, '')    
    shutil.move(f, destination_dir)


# Delete the (now empty) folders and subfolders that initially contained image files
dir_contents = glob.glob('/Volumes/ABCD/Extracted_data/*/*/ND*/sub-ND*/')
for item in dir_contents:
    print(item)
    shutil.rmtree(item)

 

####_________________________
# Quality assessment         \_______________________________________________________________
####

# CHECK SO THAT EVERY SUBJECT ONLY HAS ONE FOLDER PER MODALITY*TIMEPOINT COMBO (I.E. NO DUPLICATES
# Create data frame containing all subjects that have a T1w image

# For T1w at baseline
base_t1 = '/Extracted_data/baseline_year_1_arm_1/T1w/NDAR*/'
base = glob.glob(base_t1)
subj_t1 = pd.DataFrame(data = None, columns = ['image', 'subject'])

for f in base:
    t1_length = len(subj_t1)
    subj_img = f.split('/')[5:7]
    subj_t1.loc[t1_length] = subj_img
print(subj_t1)

# Check for duplicates
subj_t1.subject.nunique() 
len(subj_t1)


# For T2w at baseline
base_t2 = '/Extracted_data/baseline_year_1_arm_1/T2w/NDAR*/'
base = glob.glob(base_t2)

subj_t2 = pd.DataFrame(data = None, columns = ['image', 'subject'])

for f in base:
    t2_length = len(subj_t2)
    subj_img = f.split('/')[5:7]
    subj_t2.loc[t2_length] = subj_img
print(subj_t2)

# Check for duplicates
subj_t2.subject.nunique()
len(subj_t2)




####_________________________
# Zip files back up          \_______________________________________________________________
####

# After unzipping original files (from .tgz) and modifying file structure as desired, image files need to be zipped back up (into .nii.gz) to make them usable for HCP pipelines/FSL

images = glob.glob('/Extracted_data/*/*/ND*/*.nii')

# Gzip the nifti files 
for image in images:
    with open(image, 'rb') as f_in:
        with gzip.open(image + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
            
# Once all the image files are zipped back up (.gz), remove all the .nii files 
for image in images:
    if image.endswith('.nii'):
        os.remove(image)

