import fileinput
import os
import re
import sys

def create_namelists(template_dir,dat):
    templates = ['2_source_weights_var.namelist.template',
                 '3_initcd_source_to_nemo_var.namelist.template']
    namelists = ['2_{}_weights_{}.namelist'.format(dat['SOURCEID'],dat['VAR']),
                 '3_initcd_{}_to_nemo_{}.namelist'.format(dat['SOURCEID'],dat['VAR'])]
    for t,n in zip(templates,namelists):
        with open(template_dir+t) as fin, \
             open(n,'w') as fout:
            for l in fin.readlines():
                a = l 
                for d in dat:
                    a = re.sub('__'+d+'__',dat[d],a)
                fout.write(a)
            fin.close()
            fout.close()
    return

data = {
        'SOURCEID':'woa18',
        'STIMEVAR':'time',
        'SLONVAR':'lon',
        'SLATVAR':'lat',
        'SZVAR':'depth',
        'TARGETID': 'AMM15',
        'TAG': 'LBC',
        'DOMAIN': 'mesh_mask.nc'
       }


vars = {'n_an': {'SFILE': 'n_an_woa18-woa18_LBC.nc',
               'VARL': 'Nitrate',
               'OVAR': 'nitrate',
               'SCALE': '1.0'
               },   
        'i_an': {'SFILE': 'i_an_woa18-woa18_LBC.nc',
               'VARL': 'Silicate',
               'OVAR': 'silicate',
               'SCALE': '1.0'
               },   
        'p_an': {'SFILE': 'p_an_woa18-woa18_LBC.nc',
               'VARL': 'Phosphate',
               'OVAR': 'phosphate',
               'SCALE': '1.0'
               },
        'o_an': {'SFILE': 'o_an_woa18-woa18_LBC.nc',
               'VARL': 'Oxygen',
               'OVAR': 'oxygen',
               'SCALE': '1.0'
               }}

for i,v in enumerate(vars):
    create_namelists(sys.argv[1],{'VAR':v, **data, **vars[v]})
    
    if i == 0:
        os.system('sh ./interp_LBC_initial.sh {} {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID'], data['STIMEVAR']))
    else:
        os.system('sh ./interp_LBC_additional.sh {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID']))
