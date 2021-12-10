#!/sr/bin/env python3
'''
Script to download and interpolate Nitrogen deposition data from EMEP

N3flux - Total Oxidized
N4flux - Reduced Nitrogen Flux

'''
import xarray as xr
import datetime
import getpass
import os

######## User parameters ########################

# Define grid file and rename lon/lat fields
gridname = 'AMM15'
gridfile = 'mesh_mask.nc'
var_map = {'nav_lon':'lon','nav_lat':'lat','tmask':'mask'}


# Define Time Period (-/+ 1 applied to get years before and after)
ystart=2016
yend=2018
time_res='month' # year, month, day or hour

## EMEP file parameters
# As of Oct-2021, files have the format:
# {GRID}_{MODEL VERSION}_{TIME RESOLUTION}.{YEAR}met_{EMISSION YEAR}emis_({REPORTING YEAR}).nc
# Except for most recent year, which does not include reporting year in file name
rep_year=2021
emep_grid='EMEP01'
model='rv4.42'
last_emission_year=2019
url = f'https://thredds.met.no/thredds/dodsC/data/EMEP/%s_Reporting' %rep_year

#################################################

# Load dataset
url_list = []
for year in range(ystart,yend+1):
    if year==last_emission_year:
        url_list.append(f'%s/%s_%s_%s.%smet_%semis.nc' \
                    %(url,emep_grid,model,time_res,year,year))
    else:
        url_list.append(f'%s/%s_%s_%s.%smet_%semis_rep%s.nc' \
                    %(url,emep_grid,model,time_res,year,year,rep_year))
ds = xr.open_mfdataset(url_list)

# Set conversion to seconds
if time_res=='year':
    t2sec = 86400*365
elif time_res=='month':
    t2sec = 86400*30
elif time_res=='day':
    t2sec = 86400
else:
    t2sec = 3600 

# Calculate Fluxes
ds['N3_flux'] = (ds['DDEP_OXN_m2Grid'] + ds['WDEP_OXN'])/(14.007*t2sec)
ds['N3_flux'] = ds['N3_flux'].assign_attrs({'units':'mmol*m-2*s-1','long_name':'Oxidized Nitrogen Flux'})
ds['N4_flux'] = (ds['DDEP_RDN_m2Grid'] + ds['WDEP_RDN'])/(14.007*t2sec)
ds['N4_flux'] = ds['N4_flux'].assign_attrs({'units':'mmol*m-2*s-1','long_name':'Reduced Nitrogen Flux'})
ds = ds[['N3_flux','N4_flux']]

# Interpolate to grid
grid_ds = xr.open_dataset(gridfile).rename(var_map)
ds = ds.interp(lon=grid_ds.lon,lat=grid_ds.lat,method="linear")
ds['N3_flux'] = ds.N3_flux.where(grid_ds.mask.isel(t=0,z=0) == 1)
ds['N4_flux'] = ds.N4_flux.where(grid_ds.mask.isel(t=0,z=0) == 1)

# Assign Attributes
ds.attrs = {'title':f'Atmospheric nitrogen deposition from EMEP on %s grid' %gridname,
                      'institution':'Plymouth Marine Laboratory, UK',
                      'date_created': datetime.date.today().strftime('%d/%m/%Y'), 
                      'created_by': getpass.getuser(),
                      'EMEP_grid': emep_grid,
                      'model_version': model,
                      'reporting_year': rep_year}

# Save out
for year,idx in ds.groupby('time.year').groups.items():
    ofile=f'%s/%s-EMEP-NDeposition_y%s.nc' %(os.environ['OUT_DIR']+'/SBC',gridname,year)
    print('Saving '+ofile)
    ds.isel(time=idx).to_netcdf(ofile,unlimited_dims='time')
