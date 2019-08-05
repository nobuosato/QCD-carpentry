#!/usr/bin/env python
import sys
from numpy.random import choice, randn
import numpy as np
import copy
import reader
from reader import conf
import pdf,ppdf,idis

def percent_to_absolute(tabs):
    for k in tabs:
        ucorr = [x for x in tabs[k] if '_u' in x and '%' in x]
        corr  = [x for x in tabs[k] if '_c' in x and '%' in x]
        if  len(ucorr)!=0:
            for name in ucorr:
                mod_name=name.replace('%','')
                tabs[k][mod_name]=tabs[k]['value'] * tabs[k][name]/100.0
        if  len(corr)!=0:
            for name in corr:
                mod_name=name.replace('%','')
                tabs[k][mod_name]=tabs[k]['value'] * tabs[k][name]/100.0
    return tabs

def add_columns(tabs):
    for k in tabs:
        npts=len(tabs[k]['value'])
        tabs[k]['thy']=np.zeros(npts)
        tabs[k]['N']=np.zeros(npts)
        tabs[k]['residuals']=np.zeros(npts)
    return tabs

def get_alpha(tabs):
    for k in tabs:
        npts=len(tabs[k]['value'])
        alpha2=np.zeros(npts) 
        ucorr = [x for x in tabs[k] if '_u' in x and '%' not in x]
        for kk in ucorr: alpha2+=tabs[k][kk]**2
        tabs[k]['alpha']=alpha2**0.5
    return tabs

def setup_tabs(tabs):
    tabs=percent_to_absolute(tabs)
    tabs=add_columns(tabs)
    tabs=get_alpha(tabs)
    return tabs

def _get_residuals(tabs):
    for idx in tabs:
        npts=len(tabs[idx]['value'])
        for i in range(npts):
            tar=tabs[idx]['target'][i]
            Q2=tabs[idx]['Q2'][i]
            x=tabs[idx]['X'][i]

            if tabs[idx]['obs'][i]=='F2':
                thy=idis.get_F2(x,Q2,tar)   
            elif tabs[idx]['obs'][i]=='F2d/F2p':
                thy=idis.get_F2(x,Q2,'d')/idis.get_F2(x,Q2,'p')
            elif tabs[idx]['obs'][i]=='A1':
                thy=idis.get_A1(x,Q2,tar)

            tabs[idx]['thy'][i]=thy
            exp=tabs[idx]['value'][i]
            alpha=tabs[idx]['alpha'][i]
            tabs[idx]['residuals'][i]=(exp-thy)/alpha
    return tabs            

def set_new_params(par,dist):
    if dist=='pdf':
        pdf.set_params(par)
        pdf.set_sumrules()
        pdf.set_moms()
    if dist=='ppdf':
        ppdf.set_params(par)
        ppdf.set_sumrules()
        ppdf.set_moms()

def get_residuals(par,dist,tabs,verb=False):
    set_new_params(par,dist)
    res=[]
    _get_residuals(tabs)
    for idx in tabs:
        res=np.append(res,tabs[idx]['residuals'])
    print np.sum(res**2),res.size,par
    return res

if __name__ == "__main__":

    pdf.set_sumrules()
    pdf.set_moms()
    ppdf.set_sumrules()
    ppdf.set_moms()

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
    tabs1=reader.load_data_sets('idis')
    tabs1=setup_tabs(tabs1)
    
    ##--inclusive polarized DIS
    #conf['datasets']['pidis']={}
    #conf['datasets']['pidis']['xlsx']={}
    #conf['datasets']['pidis']['xlsx'][10001]='pidis/expdata/10001.xlsx' # 10001 | deuteron | A1   | COMPASS   
    #conf['datasets']['pidis']['xlsx'][10033]='pidis/expdata/10033.xlsx' # 10033 | deuteron | A1   | SMC       
    #conf['datasets']['pidis']['xlsx'][10034]='pidis/expdata/10034.xlsx' # 10034 | deuteron | A1   | SMC       
    #conf['datasets']['pidis']['xlsx'][10002]='pidis/expdata/10002.xlsx' # 10002 | proton   | A1   | COMPASS   
    #conf['datasets']['pidis']['xlsx'][10003]='pidis/expdata/10003.xlsx' # 10003 | proton   | A1   | COMPASS   
    #conf['datasets']['pidis']['xlsx'][10004]='pidis/expdata/10004.xlsx' # 10004 | proton   | A1   | EMC       
    #conf['datasets']['pidis']['xlsx'][10035]='pidis/expdata/10035.xlsx' # 10035 | proton   | A1   | SMC       
    #conf['datasets']['pidis']['xlsx'][10036]='pidis/expdata/10036.xlsx' # 10036 | proton   | A1   | SMC       
    #conf['datasets']['pidis']['filters']=[]
    #conf['datasets']['pidis']['filters'].append("Q2>1.69") 
    #conf['datasets']['pidis']['filters'].append("W2>10.0") 
    #tabs2=reader.load_data_sets('pidis')
    #tabs2=setup_tabs(tabs2)
    
    par=pdf.get_params() 

    print get_residuals(par,'pdf',tabs1)








