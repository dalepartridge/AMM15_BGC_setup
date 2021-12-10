import fileinput
import os
import re
import sys

def create_namelists(template_dir,dat):
    templates = ['1_initcd_source_to_source_var_irregular.namelist.template2D',
                 '2_source_weights_var.namelist.template2D',
                 '3_initcd_source_to_nemo_var.namelist.template2D']
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

ben_dict = {'Y2':{'c'}, 'Y3':{'c'}, 'Y4':{'c'}, 
            'H1':{'c'}, 'H2':{'c'},
            'K3':{'n'}, 'K4':{'n'}, 'K1':{'p'}, 'K5':{'s'},
            'G2':{'o','o_deep'}, 'G3':{'c'}, 
            'Q1':{'c','n','p'}, 'Q6':{'c','n','p','s',
            'pen_depth_c','pen_depth_n','pen_depth_p','pen_depth_s'},
            'Q7':{'c','n','p','pen_depth_c','pen_depth_n','pen_depth_p'},
            'Q17':{'c','n','p'}, 'ben_col':{'D1m','D2m'}, 'bL2':{'c'}, 'ben_nit':{'G4n'}}

vars={}
for v in ben_dict:
    for k in ben_dict[v]:
        vl = 'fabm_st2Dn'+v+'_'+k
        vars[vl] = {'SFILE': 'amm7_restart_trc.nc',
                'VARL': '',
                'OVAR': vl,
                'SCALE': '1.0'}

for i,v in enumerate(vars):
    create_namelists(sys.argv[1],{'VAR':v, **data, **vars[v]})
    if i == 0:
        os.system('sh ./interp_IC_initial.sh {} {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID'], data['STIMEVAR']))
    else:
        os.system('sh ./interp_IC_additional.sh {} {} {}'.format(v, vars[v]['SFILE'], data['SOURCEID']))


