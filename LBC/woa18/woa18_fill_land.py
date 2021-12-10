import xarray as xr
import pandas as pd
import numpy as np

df = pd.read_csv('WOA18_fill_land_mapping.csv')
lnames = ['nitrate','oxygen','silicate','phosphate']
vars = ['n_an','o_an','i_an','p_an']
for ln,var in zip(lnames,vars):

    fname = 'woa18_%s_monthly_depth.nc' %ln
    ds = xr.open_dataset(fname,decode_times=False)
    
    for k in range(ds.depth.size):
        df_k = df.loc[df['depth']==k]
        for t in range(ds.time.size):
            ds[var].values[t,k,df_k.woa18_land_lat.values,df_k.woa18_land_lon.values] = ds[var].values[t,k,df_k.woa18_nn_lat,df_k.woa18_nn_lon]
    ds.to_netcdf(var+'_woa18-woa18_LBC.nc')
