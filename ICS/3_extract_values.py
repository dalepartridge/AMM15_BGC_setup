#!/usr/bin/env python

'''
Extract interpolated fields and put them in the 
newly created restart_trc file. Some QC to ensure
no bad values from interpolation
'''

import netCDF4
import numpy as np

masknc = netCDF4.Dataset('mesh_mask.nc')
mask = masknc.variables['tmask'][:]
masknc.close()

outfile = 'bgc_ini.nc'
nco = netCDF4.Dataset(outfile,'a')

pel_dir = 'interp_AMM7_to_AMM15/pelagic/'
pel_dict = {'N3':{'n'}, 'N4':{'n'}, 'N1':{'p'}, 'N5':{'s'},
            'O2':{'o'}, 'O3':{'c','bioalk'},
            'P1':{'Chl','c','n','p','s'},
            'P2':{'Chl','c','n','p'},
            'P3':{'Chl','c','n','p'},
            'P4':{'Chl','c','n','p'},
            'Z4':{'c'}, 'Z5':{'c','n','p'},
            'Z6':{'c','n','p'},
            'R1':{'c','n','p'}, 'R2':{'c'}, 'R3':{'c'},
            'R4':{'c','n','p'}, 'R6':{'c','n','p','s'},
            'R8':{'c','n','p','s'},
            'L2':{'c'}, 'B1':{'c','n','p'}, 'light':{'ADY'}}

ben_dir = 'interp_AMM7_to_AMM15/benthic/'
ben_dict = {'Y2':{'c'}, 'Y3':{'c'}, 'Y4':{'c'},
            'H1':{'c'}, 'H2':{'c'},
            'K3':{'n'}, 'K4':{'n'}, 'K1':{'p'}, 'K5':{'s'},
            'G2':{'o','o_deep'}, 'G3':{'c'},
            'Q1':{'c','n','p'}, 'Q6':{'c','n','p','s',
            'pen_depth_c','pen_depth_n','pen_depth_p','pen_depth_s'},
            'Q7':{'c','n','p','pen_depth_c','pen_depth_n','pen_depth_p'},
            'Q17':{'c','n','p'}, 'ben_col':{'D1m','D2m'}, 'bL2':{'c'}, 'ben_nit':{'G4n'}}

for v in pel_dict:
    for k in pel_dict[v]:
        vl = 'TRN'+v+'_'+k
        print('Extracting: '+vl)
        nc = netCDF4.Dataset(pel_dir+vl+'_AMM7-AMM15_IC.nc')
        dat = nc.variables[vl][:]
        dat[mask==0] = 0
        dat[dat<0] = 0
        nc.close()
        nco.variables[vl][:] = dat
        nco.variables[vl.replace('TRN','TRB')][:] = dat

for v in ben_dict:
    for k in ben_dict[v]:
        vl = 'fabm_st2Dn'+v+'_'+k
        print('Extracting: '+vl)
        nc = netCDF4.Dataset(ben_dir+'initcd_'+vl+'_filled.nc')
        dat = nc.variables[vl][:]
        dat[mask[:,0,:,:]==0] = 0
        dat[dat<0] = 0
        nc.close()
        nco.variables[vl][:] = dat
        nco.variables[vl.replace('2Dn','2Db')][:] = dat

nco.close()

