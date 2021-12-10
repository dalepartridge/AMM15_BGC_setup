import xarray as xr
import pandas as pd
import numpy as np

df = pd.read_csv('GLODAP_land_fill_mapping.csv')
for var in ['TAlk','TCO2']:

    fname = 'GLODAPv2.2016b.'+var+'.reordered.nc'
    ds = xr.open_dataset(fname)

    for k in range(ds.depth_surface.size):
        df_k = df.loc[df['depth']==k]
        ds[var].values[k,df_k.glodap_land_lat.values,df_k.glodap_land_lon.values] = \ 
                        ds[var].values[k,df_k.glodap_nn_lat,df_k.glodap_nn_lon]
    ds = ds.rename({'depth':'depth_surface'}).rename_dims({'depth_surface':'depth'})
    ds = ds.rename({'depth_surface':'depth'}).assign_coords({'depth':ds.depth})[[var]]
    ds = ds.expand_dims(time=np.array([204.5]))
    ds['time'].attrs['units'] = 'months since 2000-01-01 00:00:00'
    ds.to_netcdf(var+'_glodap-glodap_LBC.nc')
