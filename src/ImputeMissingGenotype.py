# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 12:34:23 2022

@author: soibamb
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

import pandas as pd
import numpy as np
import copy
import re
from pyod.models.knn import KNN
from pyod.models.pca import PCA
from pyod.models.ecod import ECOD 
from pyod.models.iforest import IForest
from pyod.models.combination import aom, moa, average, maximization
from pyod.utils.utility import standardizer
from pythresh.thresholds.filter import FILTER
from pythresh.thresholds.meta import META
from pythresh.thresholds.clf import CLF

from joblib import Parallel, delayed, parallel_backend
import multiprocessing as mp


import warnings

def split_chromosomes(df):
    chr_uniq = df.iloc[:,0].value_counts()
    chrs = chr_uniq.keys().to_list()
    count = [chr_uniq[key] for key in chrs]
    
    '''
    print("\n=======================================================================\n")
    print("Number of chromosomes detected : ",len(chrs))
    print("\n=======================================================================\n")
    print("Number of locations in each chromosomes ")
    print(pd.DataFrame(chr_uniq))
    '''
    return(chrs,count)

'''
Read genotype data
'''
def ReadGenotype(GenotypeFile):
    df = pd.read_csv(GenotypeFile)
    '''
    print("\n=======================================================================\n")
    print("Number of individuals detected : ", df.shape[1]-2)
    print("\n=======================================================================\n")
    print("Individuals: ")
    print(df.columns[2:].to_list())
   '''
    chrs,count = split_chromosomes(df)
    return (df,chrs,count)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        
def smooth_numpy_to_genotype(snp):
    snp_tmp_1 = snp.iloc[:,0:2].copy(deep=True)
    snp_tmp_2 = snp.iloc[:,2:].copy(deep=True)
    snp_tmp_2 = snp_tmp_2.replace([3],'A')
    snp_tmp_2 = snp_tmp_2.replace([2],'B')
    snp_tmp_2 = snp_tmp_2.replace([1],'X')
    snp_tmp_2 = snp_tmp_2.replace([0],'-')  # missing items
    snp_tmp = pd.concat([snp_tmp_1,snp_tmp_2],axis=1)
    return(snp_tmp)

#df = position,genotype
def anomaly_detection_one_column(df_col,X_train1,anomaly_algo='iforest',threshold_algo='meta'):
    
    if threshold_algo == 'meta':
        thres=META()
    elif threshold_algo == 'filter':
        thres = FILTER()
    elif threshold_algo == 'clf':
        thres = CLF()
    else:
        print('thresholding algorithm choice has to be one of the three options: meta, filter, clf')
        exit()
    
    if anomaly_algo == 'iforest':
        isft=IForest()
    elif threshold_algo == 'knn':
        isft=KNN()
    elif threshold_algo == 'pca':
        isft=PCA()
    elif threshold_algo == 'ecod':
        isft=ECOD()
    else:
        print('anomaly detection algorithm choice has to be one of the four options: meta, filter, clf')
        exit()   
    
    X_train = pd.concat([X_train1,df_col],axis=1)
    X = X_train.copy(deep=True)
    X_train = pd.get_dummies(X_train, columns=[X_train.columns[1]])
    X_train = X_train.to_numpy()
    
    
    #isft = IForest()
    isft.fit(X_train)
    y_train_scores = isft.decision_function(X_train)
    y_train_pred = thres.eval(y_train_scores)
    X.iloc[y_train_pred == 1,1] = '-'
    return X.iloc[:,1].to_list()
    

def anomaly_detection_apply(df):
    warnings.filterwarnings("ignore")

    X_train = copy.deepcopy(df.iloc[:,1])
    #print(X_train)
    Res = df.iloc[:,2:].apply(anomaly_detection_one_column,args=(X_train,'iforest','meta'))
    return Res



'''
smooth_df: chrom,pos,samples .....
'''
    
def FillMissingGenotype_one_column(SMOOTH_df_col,X_train1,num_neighbors = 'auto'):
    
        y_train = SMOOTH_df_col[SMOOTH_df_col != '-']
        X_train = copy.deepcopy(X_train1[np.where(SMOOTH_df_col !='-') ])
        X_test = copy.deepcopy(X_train1[np.where(SMOOTH_df_col =='-')])
        if X_test.shape[0] > 0:
        
          
          if num_neighbors == 'auto':
              k_range = list(range(15, 35,2))
              param_grid = dict(n_neighbors=k_range)
              knn = KNeighborsClassifier(weights='uniform')
              grid = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
              grid.fit(np.reshape(X_train,(X_train.shape[0],1)), y_train)
              y_test = grid.predict(np.reshape(X_test,(X_test.shape[0],1)))
          else:
              neigh = KNeighborsClassifier(num_neighbors,weights='uniform')
              neigh.fit(np.reshape(X_train,(X_train.shape[0],1)), y_train)
              y_test = neigh.predict(np.reshape(X_test,(X_test.shape[0],1)))
          
          
        
          #combine non missing and predicted missing items
          pos = np.concatenate((X_train,X_test))
          genotype = np.concatenate((y_train,y_test))
          df_tmp = pd.DataFrame(columns=['POS','genotype'])
          df_tmp['POS']=pos
          df_tmp['genotype'] = genotype
          #order based on position in the chromosome
          df_tmp = df_tmp.sort_values(by='POS')
         # print("df_tmp")
         # print(df_tmp)
          return df_tmp['genotype'].to_list()
          #X[col] = df_tmp['genotype'].to_list()
          #val = df_tmp['genotype'].to_list()


    #return X
def FillMissingGenotype_apply(SMOOTH_df,num_neighbors = 31):
    warnings.filterwarnings("ignore")
    X_train = copy.deepcopy(SMOOTH_df.iloc[:,1].to_numpy())
    Res = SMOOTH_df.iloc[:,2:].apply(FillMissingGenotype_one_column,args=(X_train,'auto'))
    return Res


# Generate output files

def generate_output_files(new_df,ori_df):
    
    df_stats = pd.DataFrame(index=['A->B','A->X','B->A','B->X','- -> A', '- > B', '- -> X'],columns=ori_df.columns[2:])
    for i in range(2,new_df.shape[1]):
        A_B = ((ori_df.iloc[:,i] == 'A') & (new_df.iloc[:,i] == 'B').astype(bool)).sum().sum()
        A_X = ((ori_df.iloc[:,i] == 'A') & (new_df.iloc[:,i] == 'X').astype(bool)).sum().sum()
        B_A = ((ori_df.iloc[:,i] == 'B') & (new_df.iloc[:,i] == 'A').astype(bool)).sum().sum()
        B_X = ((ori_df.iloc[:,i] == 'B') & (new_df.iloc[:,i] == 'X').astype(bool)).sum().sum()       
        _A = ((ori_df.iloc[:,i] == '-') & (new_df.iloc[:,i] == 'A').astype(bool)).sum().sum()
        _B = ((ori_df.iloc[:,i] == '-') & (new_df.iloc[:,i] == 'B').astype(bool)).sum().sum()  
        _X = ((ori_df.iloc[:,i] == '-') & (new_df.iloc[:,i] == 'X').astype(bool)).sum().sum()
        df_stats.iloc[:,i-2] = [A_B,A_X,B_A,B_X,_A,_B,_X]
    return df_stats


'''
Count homozygosity and heterozygosity one sample
'''
def homo_count_one_sample(val):
    homo_ref_count = sum([1 for x in val if re.search(r"[A]",x) ])
    homo_alt_count = sum([1 for x in val if re.search(r"[B]",x) ])
    miss_count = sum([1 for x in val if re.search(r"[-]",x) ])
    hetero_count = sum([1 for x in val if re.search(r"[X]",x) ])
    return(homo_ref_count, homo_alt_count, hetero_count, miss_count)

'''
Count homozygosity and heterozygosity all samples
'''
def homo_count_all_samples(snp):

    homo_stats_df = pd.DataFrame(columns=snp.columns[2:],index=['A_count', 'B_count', 'X_count', 'miss_count'])
    for col in snp.columns[2:]:
        homo_stats_df[col] = homo_count_one_sample(snp[col].tolist())
        
    homo_stats_df_T = homo_stats_df.T
    homo_stats_df_T['A_count_perc'] = homo_stats_df_T['A_count']/homo_stats_df_T.sum(axis=1)
    homo_stats_df_T['B_count_perc'] = homo_stats_df_T['B_count']/homo_stats_df_T.sum(axis=1)
    homo_stats_df_T['H_count_perc'] = homo_stats_df_T['X_count']/homo_stats_df_T.sum(axis=1)
    homo_stats_df_T['miss_count_perc'] = homo_stats_df_T['miss_count']/homo_stats_df_T.sum(axis=1)
    #homo_stats_df_T['S_count_perc'] = homo_stats_df_T['S_count']/homo_stats_df_T.sum(axis=1)
    return(homo_stats_df_T)