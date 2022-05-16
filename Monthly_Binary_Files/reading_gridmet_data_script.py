import numpy as np
import pandas as pd
import os
import sys 

# /home/pallavi.sharma1/python_scripts
# Folder Path
#path = "C:\\Users\\Pallavi\\historical"

filename="/home/pallavi.sharma1/Rangeland_scripts/grid_names_4.txt"
with open(filename) as file:
  lines = [i.strip() for i in file]

def q90(x):
    return x.quantile(0.9)

def read_binary_file(file_path):
    dt = np.dtype([
        ('PPT','<u2'),
        ('TMAX','<i2'),
        ('TMIN','<i2'),
        ('WIND','<i2'),
        ('SPH','<i2'),
        ('SRAD','<i2'),
        ('RMAX','<i2'),
        ('RMIN','<i2')
        ])
    with open(file_path,'rb') as f:
        b = f.read()    
    date_rng = pd.date_range(start='1979-01-01', end='2019-12-31', freq='D')
    np_data = np.frombuffer(b,dt)
    df = pd.DataFrame(np_data)
    df['Date'] = date_rng
    df['PPT']= df['PPT']/40
    df['TMAX']=df['TMAX']/100
    df['TMIN']=df['TMIN']/100
    df['WIND']=df['WIND']/100
    df['SPH']=df['SPH']/10000
    df['SRAD']=df['SRAD']/40
    df['RMAX']=df['RMAX']/100
    df['RMIN']= df['RMIN']/100
    df.Date = pd.to_datetime(df.Date)

    return df

def update_df(df_one,file):
    items = file.split("_")
    df_one['LAT'] = float(items[1])
    df_one['LON'] = float(items[2])
    df_one = df_one.drop(['WIND', 'SPH', 
                'SRAD'], axis=1)
    df_one['TMID'] = (df_one['TMAX']+ df_one['TMIN'])/2
    df_one['RMID'] = (df_one['RMAX']+ df_one['RMIN'])/2
    df_one['THI'] = (0.8*df_one['TMID'])+(df_one['RMID']*(df_one['TMID']-14.4)/100)+46.4
    df_one['THI_90'] = df_one['THI']
    df_one['THI_std'] = df_one['THI']
    df_one['Emergency'] = np.where(df_one.THI>84,1, 0)
    df_one['Danger'] = df_one['THI'].apply(lambda x: 1 if x>=79 and x<84 else 0)
    df_one['Alert'] = df_one['THI'].apply(lambda x: 1 if x>=75 and x<79 else 0)
    df_one['Normal'] = np.where(df_one.THI<75,1, 0)
    return df_one
    
def summarize(df_one):
    dg = df_one.groupby(pd.Grouper(key='Date', freq='1M')).agg({'PPT':'sum','TMAX':'mean','TMIN':'mean',
                                                                'TMID':'mean','RMAX':'mean','RMIN':'mean',
                                                                'RMID':'mean','LAT':'mean', 'LON':'mean',
                                                                'THI':'mean','THI_90':q90,
                                                                'THI_std':'std','Emergency':'sum','Danger':'sum',
                                                                'Alert':'sum','Normal':'sum'})
    dg.index = dg.index.strftime('%B %Y')
    return dg

def conversion_to_binary(file,dg):
    # path for new binary files
    path1 = '/home/pallavi.sharma1/VIC_Binary_CONUS_1979_to_2019_20200721_monthly/'
    with open(path1+file+'monthly.dat', 'wb') as fh:
        fh.write(dg.to_records(index=False).tobytes())

 # grid meta data 
path="/data/adam/data/metdata/historical/UI_historical/VIC_Binary_CONUS_1979_to_2019_20200721"  
 # Change the directory
os.chdir(path)
count=0
file = lines[int(sys.argv[1])]
if file in os.listdir(path):
    file_path = path +"/" + file
    print(file)
    # call read text file function
    df_one = read_binary_file(file_path)
    df_changed = update_df(df_one,file)
    dg=summarize(df_changed)
    dg=dg.reset_index(drop=True)
    print(dg.dtypes)
    conversion_to_binary(file,dg)
