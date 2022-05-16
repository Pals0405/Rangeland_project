#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 12:24:08 2022

@author: pallavisharma
"""
# loading libraries
import numpy as np
import pandas as pd
import os
path="/home/pallavi.sharma1/VIC_Binary_CONUS_1979_to_2019_20200721_monthly"  
# Change the directory
os.chdir(path)
# reading monthly binary file
def read_monthly_binary_file(file_path):
  arr = np.fromfile(file_path,
                  dtype='f8, f8, i8, i8, f8, f8, f8, i8, f8, f8, i8, f8, f8, f8, f8, f8')
  df = pd.DataFrame(arr)
  df.columns=['RMIN','TMIN','Emergency','Danger','RMID','LAT','TMAX','Normal','RMAX','TMID','Alert','THI','PPT','LON','THI_std','THI_90']
  return df

# attaching county and state 
def create_state_county():
  # read csv file
  county = pd.read_csv("/home/pallavi.sharma1/Rangeland_scripts/County_State_pairing.csv")
  county = county.set_index('grid')
  # display DataFrame
  return county
# getting county state 
county = create_state_county() 
count=0
for file in os.listdir(path):
    print(file)
    if(count>=1):
      break
    count+=1
    file_path = path +"/" + file
    print(file)
    df_one = read_monthly_binary_file(file_path)
    df_one['County']= county["County"].loc[file]
    df_one['State']= county["State"].loc[file]
    date_rng = pd.date_range(start='1979-01-01', end='2019-12-31', freq='M')
    df_one['Date'] = date_rng
    df_one.Date = pd.to_datetime(df_one.Date)

    
df_final = df_one
count=0
# reading all the files 
for file in os.listdir(path):
    count+=1
    print(count)
    file_path = path +"/" + file
    print(file)
    df = read_monthly_binary_file(file_path)
    df['County']= county["County"].loc[file]
    df['State']= county["State"].loc[file]
    date_rng = pd.date_range(start='1979-01-01', end='2019-12-31', freq='M')
    df['Date'] = date_rng
    df.Date = pd.to_datetime(df.Date)
    df_final = pd.concat([df_final, df], axis=0)
 
print(count)
print(len(df_final))
df_final=df_final.drop_duplicates()
print(len(df_final))
dg = df_final.groupby(['County','State','Date']).mean()
#dg = dg.drop(columns=['LAT', 'LON'])
dg.reset_index(inplace=True)
dg.to_csv('/home/pallavi.sharma1/Rangeland_scripts/County_wise_THI.csv',index=False)
