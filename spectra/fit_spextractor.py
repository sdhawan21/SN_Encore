import numpy as np 
import matplotlib.pyplot as plt 
import sys, glob, os 
import pandas as pd  
import spextractor 

# written with the aim of fitting all spectra of a given SN
fstr = sys.argv[2]
f_list = glob.glob(fstr+'*')
z = float(sys.argv[1])
sn_dict = {}
sn_name = f_list[0].split('/')[-1].split('_')[0]
print("List of spectra being fitted is: ", f_list)

for filename_Ia in f_list: 
    try:
       pew, pew_err, vel, vel_err, gp_model = spextractor.process_spectra(filename_Ia, z, 
   	downsampling=3, plot=True, type='Ia',sigma_outliers=3)
       sn_dict[filename_Ia] = {}
       sn_dict[filename_Ia]['pew'] = pew
       sn_dict[filename_Ia]['pew_err'] = pew_err
       sn_dict[filename_Ia]['vel'] = vel
       sn_dict[filename_Ia]['vel_err'] = vel_err

    except:
    	print("Didnt fit ", filename_Ia)
    	sn_dict[filename_Ia] = {}
    plt.title(sn_name + ' ' + filename_Ia, fontsize=20)
    plt.savefig('plots/'+filename_Ia.split('/')[-1].split('.')[0]+'.png')
    plt.cla()

fitdir = 'fitpars/'
pd.to_pickle(sn_dict, fitdir+sn_name+'.pkl')