import xarray as xr
import pandas as pd
import numpy as np
import sys

var = sys.argv[1]

# Load AMM7, AMM15 data
ds_amm15 = xr.open_dataset('initcd_'+var+'.nc')
ds_amm7 = xr.open_dataset(var+'_AMM7-AMM7_IC.nc')

# Put into a dataframe
df = pd.read_csv('outerzone/AMM7_to_AMM15_outerzone_mapping.csv')

if 'z' in ds_amm15.dims:
    for k in range(len(ds_amm15.z)):
        ds_amm15[var].values[0,k,df.amm15_lat.values,df.amm15_lon.values]  = ds_amm7[var].values[0,k,df.amm7_lat.values,df.amm7_lon.values]
else:
    ds_amm15[var].values[0,df.amm15_lat.values,df.amm15_lon.values]  = ds_amm7[var].values[0,df.amm7_lat.values,df.amm7_lon.values]

lon = ds_amm15['lon'].values
lon[lon>180] -= 360
ds_amm15['lon'].values = lon

ds_amm15.to_netcdf('initcd_'+var+'_filled.nc')

