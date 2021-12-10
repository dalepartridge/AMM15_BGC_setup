import fileinput
import os
import re
import sys

def create_namelists(template_dir,dat):
    templates = ['1_initcd_source_to_source_var_irregular.namelist.template',
                 '2_source_weights_var.namelist.template',
                 '3_initcd_source_to_nemo_var.namelist.template']
    namelists = ['1_initcd_{}_to_{}_{}.namelist'.format(dat['SOURCEID'],dat['SOURCEID'],dat['VAR']),
                 '2_{}_weights_{}.namelist'.format(dat['SOURCEID'],dat['VAR']),
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
        'SOURCEID':'AMM7',
        'STIMEVAR':'time_counter',
        'SLONVAR':'nav_lon',
        'SLATVAR':'nav_lat',
        'SZVAR':'nav_lev',
        'TARGETID': 'AMM15',
        'TAG': 'IC',
        'DOMAIN': 'mesh_mask.nc'
       }

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


vars={}
for v in pel_dict:
    for k in pel_dict[v]:
        vl = 'TRN'+v+'_'+k
        vars[vl] = {'SFILE': 'amm7_restart_trc.nc',
                         'VARL': '',
                         'OVAR': vl,
                         'SCALE': '1.0'
                         }

for i,v in enumerate(vars):
    create_namelists(sys.argv[1],{'VAR':v, **data, **vars[v]})
    
    if i == 0:
        os.system('sh ./interp_IC_initial.sh {} {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID'], data['STIMEVAR']))
    else:
        os.system('sh ./interp_IC_additional.sh {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID']))


