#!/usr/bin/env python

'''
Convert bioalkalinity fields into TA, based on the formula

TA = 520.1 + 51.24 * S + bioalk

where S is the salinity values from the physics restart file
'''


import xarray as xr
import netCDF4
import os

ds = netCDF4.Dataset('bgc_ini.nc','a')
ds_phys = xr.open_dataset(os.environ[$OUT_DIR]+'/PHYS/restart_20161102.nc')

for v in ['TRBO3_bioalk', 'TRNO3_bioalk']:
    ds.variables[v][:] = 520.1 + 51.24 * ds_phys.sn.values + ds.variables[v][:]
ds.close()

os.system('module load nco; \ 
        ncrename -v TRBO3_bioalk,TRBO3_TA bgc_ini.nc; \
        ncrename -v TRNO3_bioalk,TRNO3_TA bgc_ini.nc')
