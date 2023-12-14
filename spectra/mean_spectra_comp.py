import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import glob 
import spectres 

from astropy.io import ascii 

spec_lowz = glob.glob('datasets/lowz/CSP_spectra_DR1/SN*.dat')
csp_meta = np.loadtxt('datasets/lowz/CSP_DR1_specMeta.dat', skiprows=10, dtype=str, 
	usecols=(0, 5, 10))

csp_meta_norm = csp_meta[csp_meta[:,-2] == 'Normal']
wv_res = np.arange(5000, 11000, 5)
fl_mean = np.zeros(len(wv_res))
fl_arr = np.zeros(len(wv_res))
spec_epoch = []

for ii in spec_lowz: 
    tt = np.loadtxt(ii, dtype=str, max_rows=6, usecols=(0,1), comments=None)
    ep = float(tt[5][1])
    #print(tt)
    specval = np.loadtxt(ii)

    if (ep >= 20) and (ep <= 30):
        spec_epoch.append([ii, ep])
        specval[:,1] /= max(specval[:,1])
        spec_res = spectres.spectres(wv_res, specval[:,0], specval[:,1])
        spec_res[np.isnan(spec_res)] = 0
        print(spec_res)
        fl_mean += spec_res
        fl_arr = np.vstack([fl_arr, spec_res])
        
print(fl_arr)
fl_std = np.std(fl_arr, axis=0)
fl_mean /= len(spec_epoch)
plt.plot(wv_res, fl_mean, label='Mean low-z (+20 - +30)')
plt.fill_between(wv_res, fl_mean - fl_std, fl_mean + fl_std, alpha=0.2, color='g', label=r'1$\sigma$ dispersion')
encore = np.loadtxt('SNEncore_restframe.ascii')
plt.plot(encore[:,0], encore[:,1]/max(encore[:,1]), label='NIRSpec: Encore')
plt.legend(loc=0)
plt.xlabel('$\lambda (\AA)$', fontsize=20, labelpad=-3)
plt.ylabel('Norm Flux ', fontsize=20, labelpad=-3)
plt.savefig('plots/encore_lowz_comp.pdf')
plt.show()
#print(spec_epoch, len(spec_epoch))