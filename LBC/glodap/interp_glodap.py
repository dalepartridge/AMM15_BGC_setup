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
        'SOURCEID':'glodap',
        'STIMEVAR':'',
        'SLONVAR':'lon',
        'SLATVAR':'lat',
        'SZVAR':'Depth',
        'TARGETID': 'AMM15',
        'TAG': 'LBC',
        'DOMAIN': 'mesh_mask.nc'
       }


vars={}
vars['TAlk'] = {'SFILE': 'TAlk_glodap-glodap_LBC.nc',
                         'VARL': 'seawater alkalinity expressed as mole equivalent per unit mass',
                         'OVAR': 'TAlk',
                         'SCALE': '1.0'
                         }
vars['TCO2'] = {'SFILE': 'TCO2_glodap-glodap_LBC.nc',
                         'VARL': 'moles of dissolved inorganic carbon per unit mass in seawater',
                         'OVAR': 'TCO2',
                         'SCALE': '1.0'
                         }

v = 'TAlk'
create_namelists(sys.argv[1],{'VAR':v, **data, **vars[v]})
os.system('sh ./interp_LBC_initial.sh {} {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID'], data['STIMEVAR']))

v = 'TCO2'
create_namelists(sys.argv[1],{'VAR':v, **data, **vars[v]})
os.system('sh ./interp_LBC_additional.sh {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID']))


