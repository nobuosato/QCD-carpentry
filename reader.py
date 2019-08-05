#!/usr/bin/env python
import sys,os
import numpy as np
import pandas as pd
import params as par
conf={}

def isnumeric(value):
    try:
        int(value)
        return True
    except:
        return False

def get_X(tab):
    cols=tab.columns.values
    if any([c=='X' for c in cols])==False:
        if any([c=='W2' for c in cols]):
            tab['X']=pd.Series(tab['Q2']/(tab['W2']-par.M2+tab['Q2']),index=tab.index)
        elif any([c=='W' for c in cols]):
            tab['X']=pd.Series(tab['Q2']/(tab['W']**2-par.M2+tab['Q2']),index=tab.index)
        else:
            print 'cannot retrive X values'
            sys.exit()
    return tab

def get_W2(tab):
    cols=tab.columns.values
    if any([c=='W2' for c in cols])==False: 
        tab['W2'] = pd.Series(par.M2 + tab.Q2/tab.X - tab.Q2,index=tab.index)
    return tab

def get_idx(tab):
    tab['idx']=pd.Series(tab.index,index=tab.index)
    return tab

def apply_cuts(tab,reaction):
    if  'filters' in conf['datasets'][reaction]:
        for f in conf['datasets'][reaction]['filters']:
            tab=tab.query(f)
    return tab

def modify_table(tab,reaction):
    tab=get_X(tab)   
    tab=get_W2(tab)   
    tab=apply_cuts(tab,reaction)
    tab=get_idx(tab)
    return tab

def load_data_sets(reaction,verb=True):
    if reaction not in conf['datasets']: return None
    XLSX=conf['datasets'][reaction]['xlsx']
    TAB={}
    for k in XLSX: 
        if verb: print 'loading %s data sets %d'%(reaction,k)
        fname=conf['datasets'][reaction]['xlsx'][k]
        tab=pd.read_excel('database/%s'%(fname))
        tab=modify_table(tab,reaction)
        npts=tab.index.size
        if npts==0: continue
        TAB[k]=tab.to_dict(orient='list')
        for kk in TAB[k]: 
            if  isnumeric(TAB[k][kk][0]):
                TAB[k][kk]=np.array(TAB[k][kk])
    return TAB

if __name__ == "__main__":

    conf['datasets']={}

    #--inclusive unpolarized DIS
    conf['datasets']['idis']={}
    conf['datasets']['idis']['xlsx']={}
    conf['datasets']['idis']['xlsx'][10010]='idis/expdata/10010.xlsx' # proton   | F2      | SLAC  
    conf['datasets']['idis']['xlsx'][10016]='idis/expdata/10016.xlsx' # proton   | F2      | BCDMS 
    conf['datasets']['idis']['xlsx'][10020]='idis/expdata/10020.xlsx' # proton   | F2      | NMC   
    conf['datasets']['idis']['xlsx'][10011]='idis/expdata/10011.xlsx' # deuteron | F2      | SLAC  
    conf['datasets']['idis']['xlsx'][10017]='idis/expdata/10017.xlsx' # deuteron | F2      | BCDMS 
    conf['datasets']['idis']['xlsx'][10021]='idis/expdata/10021.xlsx' # d/p      | F2d/F2p | NMC   
    conf['datasets']['idis']['filters']=[]
    conf['datasets']['idis']['filters'].append("Q2>1.0") 
    conf['datasets']['idis']['filters'].append("W2>4.0") 
    TAB=load_data_sets('idis')

    #--inclusive polarized DIS
    conf['datasets']['pidis']={}
    conf['datasets']['pidis']['xlsx']={}
    conf['datasets']['pidis']['xlsx'][10001]='pidis/expdata/10001.xlsx' # 10001 | deuteron | A1   | COMPASS   
    conf['datasets']['pidis']['xlsx'][10033]='pidis/expdata/10033.xlsx' # 10033 | deuteron | A1   | SMC       
    conf['datasets']['pidis']['xlsx'][10034]='pidis/expdata/10034.xlsx' # 10034 | deuteron | A1   | SMC       
    conf['datasets']['pidis']['xlsx'][10002]='pidis/expdata/10002.xlsx' # 10002 | proton   | A1   | COMPASS   
    conf['datasets']['pidis']['xlsx'][10003]='pidis/expdata/10003.xlsx' # 10003 | proton   | A1   | COMPASS   
    conf['datasets']['pidis']['xlsx'][10004]='pidis/expdata/10004.xlsx' # 10004 | proton   | A1   | EMC       
    conf['datasets']['pidis']['xlsx'][10035]='pidis/expdata/10035.xlsx' # 10035 | proton   | A1   | SMC       
    conf['datasets']['pidis']['xlsx'][10036]='pidis/expdata/10036.xlsx' # 10036 | proton   | A1   | SMC       
    conf['datasets']['pidis']['filters']=[]
    conf['datasets']['pidis']['filters'].append("Q2>1.69") 
    conf['datasets']['pidis']['filters'].append("W2>10.0") 
    TAB=load_data_sets('pidis')







