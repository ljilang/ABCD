#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 09:33:58 2021

@author: Lara
"""
########
##
# Extract random sample from complete dataset
## 
########

####_________________
# Import modules     \_______________________________________________________________
####

import os
import pandas as pd
import shutil
import glob

####___________________
# Check if files exist \_______________________________________________________________

# For Baseline 
# Define Source and Destination folder 
source = '/Extracted_data/'
dest = '/Random/'

# Create and prepare the data frame 
sample = 'q01_rand.xlsx'
sample_df = pd.read_excel(sample, index_col=0)

sample_df = sample_df.sort_values('SUBJECTKEY').reset_index().drop(['index'], axis=1)

# Set counter
counter = 0


# Loop through all folders in path to check if all subjects have a T1w and a T2w image
for sub in sample_df.index:
    
    df = sample_df.iloc[sub]

    
    # T1 
    try:     
        t1 = glob.glob(source+df.EVENTNAME_base+'/T1w/'+df.SUBJECTKEY.replace('_','')+'/*.nii.gz')[0]
        os.path.isfile(t1)
        
    except:
        counter=counter+1
        print(counter, ' | ERROR: T1w from subject:',df.SUBJECTKEY,' not found')
        
        
    # T2 
    try:     
        t2 = glob.glob(source+df.EVENTNAME_base+'/T2w/'+df.SUBJECTKEY.replace('_','')+'/*.nii.gz')[0]
        os.path.isfile(t2)
    except:
        counter=counter+1
        print(counter, ' | ERROR: T2w from subject:',df.SUBJECTKEY,' not found')
       


####_________________
# Extract folders    \_______________________________________________________________
####


# For Baseline 
# Define Source and Destination folder 
source = '/Extracted_data/'
dest = '/Random/'

# Create and prepare the data frame 
sample = '/q01_rand.xlsx'
sample_df = pd.read_excel(sample, index_col=0)

sample_df = sample_df.sort_values('SUBJECTKEY').reset_index().drop(['index'], axis=1)

# Set counter
counter = 0

# Loop through all files in path to extract image files and copy them to new subject-specific folders in dest-directory
for sub in sample_df.index:
    
    df = sample_df.iloc[sub]

    t1_notfound = 0
    t2_notfound = 0

    

    # T1 Create HCP folders 
    try:     
        t1 = glob.glob(source+df.EVENTNAME_base+'/T1w/'+df.SUBJECTKEY.replace('_','')+'/*.nii.gz')[0]
        dest_t1 = dest+t1.split('/')[6]+'/unprocessed/3T/T1w_MPR1/'+t1.split('/')[6]+'_3T_T1w_MPR1.nii.gz'
        # dest_t1 = dest+t1.split('Extracted_data/')[1]
        if not os.path.exists(os.path.dirname(dest_t1)):
             os.makedirs(os.path.dirname(dest_t1))
        
        shutil.copy(t1, dest_t1)
    except:
        print(' | ERROR: T1w from subject:',df.SUBJECTKEY,' not found')
        t1_notfound = 1
        
        
        
    # T2 Create HCP folders 
    try:     
        t2 = glob.glob(source+df.EVENTNAME_base+'/T2w/'+df.SUBJECTKEY.replace('_','')+'/*.nii.gz')[0]
        dest_t2 = dest+t2.split('/')[6]+'/unprocessed/3T/T2w_SPC1/'+t2.split('/')[6]+'_3T_T2w_SPC1.nii.gz'
        # dest_t2 = dest+t2.split('Extracted_data/')[1]
        if not os.path.exists(os.path.dirname(dest_t2)):
              os.makedirs(os.path.dirname(dest_t2))
        shutil.copy(t2, dest_t2)
    except:
        print(' | ERROR: T2w from subject:',df.SUBJECTKEY,' not found')
        t2_notfound = 1
        
        
        
        
    # Remove subjects (directories) if T1 and/or T2 are not found
    if (t1_notfound==1) and (t2_notfound==0):
        counter=counter+1
        shutil.rmtree(dest+os.path.dirname(dest_t2).split(dest)[1].split('/')[0])
        # shutil.rmtree(os.path.dirname(dest_t2))
        print(counter,'   => SUBJECT REMOVED!')

    if (t1_notfound==0) and (t2_notfound==1):
        counter=counter+1
        shutil.rmtree(dest+os.path.dirname(dest_t1).split(dest)[1].split('/')[0])
        # shutil.rmtree(os.path.dirname(dest_t1))
        print(counter,'   => SUBJECT REMOVED!')    

    if (t1_notfound==1) and (t2_notfound==1):
        counter=counter+1
        print(counter,'   => SUBJECT DOES NOT EXIST!')  
    
