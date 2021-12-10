### AMM7 biogeochemical lateral open boundaries
### The script applies seasonality to annual climatology of DIC and Alkalinity retrieved from GLODAPv2 based on monthly mean climatology values of nitrate from WOA18. This assumes DIC/Alkalinity seasonality driven by biogeochemical processes only. Script originally created by Gennadi Lessin, modified by Helen Powley

import xarray as xr
import numpy as np

# Load data 
ds_nit = xr.open_dataset('woa18/nitrate_woa18-AMM15_LBC.nc')

ds_talk=xr.open_dataset('glodap/TAlk_glodap-AMM15_LBC.nc').squeeze().expand_dims({'time_counter':12})
ds_talk=ds_talk.drop('time_counter').assign_coords({'time_counter':ds_nit.time_counter}) 

ds_dic=xr.open_dataset('glodap/TCO2_glodap-AMM15_LBC.nc').squeeze().expand_dims({'time_counter':12})
ds_dic=ds_dic.drop('time_counter').assign_coords({'time_counter':ds_nit.time_counter}) 

# Calculate seasonal nitrate anomaly
nit_anom=ds_nit.nitrate - ds_nit.nitrate.mean('time_counter')

#DIC - apply seasonality following Redfield ratio
ds_dic['TCO2'] = ds_dic['TCO2'] + nit_anom*106./16.
ds_talk['TAlk'] = ds_talk['TAlk'] - nit_anom
    
# Save out
ds_dic.to_netcdf('glodap/TCO2_seasonal_glodap-AMM15_LBC.nc')
ds_talk.to_netcdf('glodap/TAlk_seasonal_glodap-AMM15_LBC.nc')

