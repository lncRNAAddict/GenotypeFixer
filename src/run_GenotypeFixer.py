#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 06:57:53 2023

@author: soibamb
"""


import numpy as np
import pandas as pd
from optparse import OptionParser
import time
import random
import sys
from ImputeMissingGenotype import *




'''
Parsing input section
'''

parser = OptionParser()
parser.add_option("-g", "--genotype", action="store", type="string", dest="genotype_file",default="test")
parser.add_option("-o", "--output", action="store", type="string", dest="output_prefix",default="test")
parser.add_option("-a", "--anomaly", action="store", type="string", dest="anomaly_method",default="iforest")
parser.add_option("-t", "--thresh", action="store", type="string", dest="threshold_method",default="meta")
parser.add_option("-c", "--chrs", action="store", type="string", dest="chr_list",default="all")




(options, args) = parser.parse_args()


print("==============================================================")
print("genotype file:",options.genotype_file)
print("output prefix:",options.output_prefix)
print("anomaly detection algorithm:",options.anomaly_method)
print("thresholding algorithm:",options.threshold_method)
print("chr list to process:",options.chr_list)


genotype_file = options.genotype_file
output_prefix = options.output_prefix
anomaly_method= options.anomaly_method
threshold_method = options.threshold_method
chr_list = options.chr_list

'''
Fill missing values
'''

df,chrs,count = ReadGenotype(genotype_file)
cols = df.columns
df = df.sort_values(by=[cols[0],cols[1]])
chrs.sort()

if chr_list != 'all':
    chrs = chr_list.split(",")
    chrs.sort()
    df = df[df[cols[0]].isin(chrs)]



print("Performing Missing value imputation")
print("=========================================================\n")
df_fills =[]
for CHR in chrs:
    print(CHR)
    df_CHR = df.loc[df.iloc[:,0] == CHR,:].copy(deep=True)
    Result = FillMissingGenotype_apply(df_CHR,num_neighbors = 'auto') 
    df_CHR_ = Result.copy(deep=True)
    df_CHR_.insert(0,'chromosome',df_CHR.iloc[:,0])
    df_CHR_.insert(1,'position',df_CHR.iloc[:,1])
    df_fills.append(df_CHR_)
    

df_ = pd.concat(df_fills)


print("=========================================================\n")
print("Performing anomaly detection")
print("=========================================================\n")

#Anomaly detection

df_fills = []
for CHR in chrs:
    print(CHR)
    df_CHR = df_.loc[df_.iloc[:,0] == CHR,:].copy(deep=True)
    Result =  anomaly_detection_apply(df_CHR)
    df_CHR_ = Result.copy(deep=True)
    df_CHR_.insert(0,'chromosome',df_CHR.iloc[:,0])
    df_CHR_.insert(1,'position',df_CHR.iloc[:,1])
    df_fills.append(df_CHR_)

df_ = pd.concat(df_fills)   



#Correct anomalies


print("=========================================================\n")
print("Performing missing value Correction")
print("=========================================================\n")

df_fills = []
for CHR in chrs:
    print(CHR)
    df_CHR = df_.loc[df.iloc[:,0] == CHR,:].copy(deep=True)
    Result = FillMissingGenotype_apply(df_CHR,num_neighbors = 'auto') #FillMissingGenotype(df_CHR)
    df_CHR_ = Result.copy(deep=True)
    df_CHR_.insert(0,'chromosome',df_CHR.iloc[:,0])
    df_CHR_.insert(1,'position',df_CHR.iloc[:,1])
    df_fills.append(df_CHR_)
    
    
df_corrected = pd.concat(df_fills)      


#output corrected file
df_corrected.to_csv(output_prefix+".corrected.csv",index=False)

#output corrected statistics
df_corrected_stats = generate_output_files(df_corrected,df)
df_corrected_stats.to_csv(output_prefix + '.corrected.stats.csv')

#output summary statistics/count
homo_count_all_samples(df_corrected).to_csv(genotype_file+'.summary.stats.csv')
homo_count_all_samples(df_).to_csv(output_prefix +'.summary.stats.csv')





        

    
    
    

