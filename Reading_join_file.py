#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 20:02:07 2022

@author: pallavisharma
"""

import numpy as np
import pandas as pd
import os
from collections import defaultdict
import sys
# storing file names in dictionary
#/home/pallavi.sharma1/grid_files_names

counT=0
dictionary=defaultdict()
for file in os.listdir("/home/pallavi.sharma1/grid_files_names"):
  dictionary[counT]=str(file)
  counT+=1


path="/home/pallavi.sharma1/VIC_Binary_CONUS_1979_to_2019_20200721_monthly"  
# Change the directory
os.chdir(path)
def read_monthly_binary_file(file_path):
  arr = np.fromfile(file_path,
                  dtype='f8, f8, i8, i8, f8, f8, f8, i8, f8, f8, i8, f8, f8, f8, f8, f8')
  df = pd.DataFrame(arr)
  df.columns=['RMIN','TMIN','Emergency','Danger','RMID','LAT','TMAX','Normal','RMAX','TMID','Alert','THI','PPT','LON','THI_std','THI_90']
  return df

filer = dictionary[sys.argv[1]]
filename="/home/pallavi.sharma1/grid_files_names/"+filer
with open(filename) as file:
  lines = [i.strip() for i in file]

count=0
for file in os.listdir(path):
    if file in lines:
        print(file)
        if(count>=1):
          break
        count+=1
        file_path = path +"/" + file
        print(file)
        df_one = read_monthly_binary_file(file_path)
        date_rng = pd.date_range(start='1979-01-01', end='2019-12-31', freq='M')
        df_one['Date'] = date_rng
        df_one.Date = pd.to_datetime(df_one.Date)

    
df_final = df_one
 
# reading all the files 
for file in os.listdir(path):
    if file in lines:
        file_path = path +"/" + file
        print(file)
        df = read_monthly_binary_file(file_path)
        date_rng = pd.date_range(start='1979-01-01', end='2019-12-31', freq='M')
        df['Date'] = date_rng
        df.Date = pd.to_datetime(df.Date)
        df_final = pd.concat([df_final, df], axis=0)
 
print(count)
print(len(df_final))
df_final=df_final.drop_duplicates()
print(len(df_final))
county = pd.read_csv("/home/pallavi.sharma1/Rangeland_join_scripts/join_new_df.csv")
df_final = pd.merge(df_final, county,  how='inner', on=['LAT','LON'])
dg = df_final.groupby(['County','State','Date']).mean()
dg.reset_index(inplace=True)
dg.to_csv('/home/pallavi.sharma1/output_files/County_wise_THI'+filer+'.csv',index=False)
