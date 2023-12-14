import numpy as np 
import matplotlib.pyplot as plt 
import glob, os, sys 
import pandas as pd 

par = sys.argv[1]
par_arr = ['vel', 'pew']
feat = sys.argv[2]
feat_arr = ['left', 'right']
if feat == 'left':
	tag = '5972'
elif feat == 'right':
	tag = '6355'

if par == 'vel':
    str_fn ='folatelli_2013/SN200*exp*'
    col_vals = (1,-6, -5)
    str_par = 'vel'
    frac  = 1e3
else: 
    str_fn = 'folatelli_2013/SN200*ew*'
    col_vals = (1,-4, -3)
    str_par = 'pew'
    frac = 1
plt.figure(figsize=(8,6))
gl = glob.glob(str_fn)
vel_evol = []
for fname in gl: 
    vel_spec=  np.loadtxt(fname, usecols=col_vals)
    if len(np.shape(vel_spec)) > 1:
        vel_spec_gd = vel_spec[vel_spec[:,1] > 0]
        for ii in vel_spec_gd: 
            vel_evol.append([ii[0], ii[1], ii[2]])

encore_vals = pd.read_pickle('fitpars/m0138.pkl')
print(np.shape(vel_evol))
vel_evol = np.array(vel_evol)
print(encore_vals)
plt.errorbar(vel_evol[:,0], vel_evol[:,1], vel_evol[:,2], fmt='b.', ms=2)
plt.errorbar(27.2, encore_vals['m0138_sn_3.flm'][str_par][feat]  * frac,  
	xerr=5.5, yerr =  encore_vals['m0138_sn_3.flm'][str_par+'_err'][feat]* frac, fmt='kD', ms=5)

plt.xlabel('Phase (days)', fontsize=20, labelpad=-3)
plt.ylabel(str_par+'_'+ feat +' (km s$^{-1}$) ', fontsize=20, labelpad=-3)
plt.savefig('plots/'+str_par+'_evol_SiII'++'.pdf')
plt.show()