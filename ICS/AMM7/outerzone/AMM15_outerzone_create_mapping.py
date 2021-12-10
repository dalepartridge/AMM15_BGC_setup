import xarray as xr
import pandas as pd
import numpy as np

# Load AMM7, AMM15 and the mask of points outside the region
ds_amm15 = xr.open_dataset('initcd_TRNN3_n.nc').isel(time_counter=0,z=0)
ds_mask = xr.open_dataset('AMM15_AMM7_outerzone_mask.nc').isel(time=0,z=0)
ds_amm7 = xr.open_dataset('TRNN3_n_AMM7-AMM7_ICS.nc').isel(time=0,z=0)

# Find all indices of points in AMM15 outside of AMM7 domain
y_amm15,x_amm15 = np.where(ds_mask.mask.values == 1)

# Find nearest index of points in AMM7 
x_amm7,y_amm7 = nearest_indices_2D(ds_amm7.nav_lon,ds_amm7.nav_lat,
                                    ds_amm15.lon.values[y_amm15,x_amm15],
                                    ds_amm15.lat.values[y_amm15,x_amm15])

#Ensure those points are not the boundary layer
x_amm7[x_amm7==0] += 1
y_amm7[y_amm7==0] += 1

# Put into a dataframe
idx_df = pd.DataFrame(data={'amm15_lon':x,'amm15_lat':y,'amm7_lon':x_amm7,'amm7_lat':y_amm7})
idx_df.to_csv('AMM7_to_AMM15_outerzone_mapping.csv')

def nearest_indices_2D(mod_lon, mod_lat, new_lon, new_lat):
    '''
    Obtains the 2 dimensional indices of the nearest model points to specified
    lists of longitudes and latitudes. Makes use of sklearn.neighbours
    and its BallTree haversine method. Function taken from COAsT
    Example Useage
    ----------
    # Get indices of model points closest to altimetry points
    ind_x, ind_y = nemo.nearest_indices(altimetry.dataset.longitude,
    altimetry.dataset.latitude)
    # Nearest neighbour interpolation of model dataset to these points
    interpolated = nemo.dataset.isel(x_dim = ind_x, y_dim = ind_y)
    Parameters
    ----------
    mod_lon (2D array): Model longitude (degrees) array (2-dimensional)
    mod_lat (2D array): Model latitude (degrees) array (2-dimensions)
    new_lon (1D array): Array of longitudes (degrees) to compare with model
    new_lat (1D array): Array of latitudes (degrees) to compare with model
    Returns
    -------
    Array of x indices, Array of y indices
    '''
    import sklearn.neighbors as nb
    
    # Cast lat/lon to numpy arrays in case xarray things
    new_lon = np.array(new_lon)
    new_lat = np.array(new_lat)
    mod_lon = np.array(mod_lon)
    mod_lat = np.array(mod_lat)
    original_shape = mod_lon.shape
    
    # If a mask is supplied, remove indices from arrays.
    mod_lon = mod_lon.flatten()
    mod_lat = mod_lat.flatten()
    
    # Put lons and lats into 2D location arrays for BallTree: [lat, lon]
    mod_loc = np.vstack((mod_lat, mod_lon)).transpose()
    new_loc = np.vstack((new_lat, new_lon)).transpose()
    
    # Convert lat/lon to radians for BallTree
    mod_loc = np.radians(mod_loc)
    new_loc = np.radians(new_loc)
    
    # Do nearest neighbour interpolation using BallTree (gets indices)
    tree = nb.BallTree(mod_loc, leaf_size=5, metric='haversine')
    _, ind_1d = tree.query(new_loc, k=1)
    
    # Get 2D indices from 1D index output from BallTree
    ind_y, ind_x = np.unravel_index(ind_1d, original_shape)
    ind_x = xr.DataArray(ind_x.squeeze())
    ind_y = xr.DataArray(ind_y.squeeze())
    return ind_x, ind_y
