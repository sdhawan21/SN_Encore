import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import glob, sys 
import spectres 

from astropy.io import ascii 

nearest_epoch = float(sys.argv[1])
model_sch = sys.argv[2]
model_ddc = sys.argv[3]
model_pdd = sys.argv[4]
	
sch = glob.glob('models/SNIa_models_B17/'+model_sch+'/'+model_sch+'_*')
ddc = glob.glob('models/SNIa_models_B17/'+model_ddc+'/'+model_ddc+'_*')
pddel = glob.glob('models/SNIa_models_B17/'+model_pdd+'/'+model_pdd+'_*')
sch_ep = np.array([[ii, float(ii.split('/')[-1].split('_')[-1].split('d')[0]) - 17.1] for ii in sch])
ddc_ep = np.array([[ii, float(ii.split('/')[-1].split('_')[-1].split('d')[0]) - 17.3] for ii in ddc])
pddel_ep = np.array([[ii, float(ii.split('/')[-1].split('_')[-1].split('d')[0]) - 17.8] for ii in pddel])

sch_val, eps = sch_ep[abs(sch_ep[:,1].astype('float32') - nearest_epoch) == min(abs(sch_ep[:,1].astype('float32') - nearest_epoch))][0]
ddc_val, epd = ddc_ep[abs(ddc_ep[:,1].astype('float32') - nearest_epoch) == min(abs(ddc_ep[:,1].astype('float32') - nearest_epoch))][0]
pddel_val, epp = pddel_ep[abs(pddel_ep[:,1].astype('float32') - nearest_epoch) == min(abs(pddel_ep[:,1].astype('float32') - nearest_epoch))][0]

print("Epochs are (for SCH, DDC, PDDEL): ", sch_ep[:,1], ddc_ep[:,1], pddel_ep[:,1])
encore = np.loadtxt('SNEncore_restframe.ascii')
sch_spec = np.loadtxt(sch_val)
ddc_spec = np.loadtxt(ddc_val)
pddel_spec = np.loadtxt(pddel_val)

wv_res = np.arange(5500, 11000, 10)
fl_res = spectres.spectres(wv_res, encore[:,0], encore[:,1])
fl_res[np.isnan(fl_res)] = 0.
print(fl_res)
#plt.plot(encore[:,0], encore[:,1]/max(encore[:,1]), label='NIRSpec: Encore')
plt.plot(wv_res, fl_res / max(fl_res), color='saddlebrown', label='NIRSpec - Binned')
plt.plot(sch_spec[:,0], sch_spec[:,1]/max(sch_spec[:,1]), label=model_sch+' '+ str(eps))
plt.plot(ddc_spec[:,0], ddc_spec[:,1]/max(ddc_spec[:,1]), label=model_ddc+' '+ str(epd))
plt.plot(pddel_spec[:,0], pddel_spec[:,1]/max(pddel_spec[:,1]), label=model_pdd+' ' + str(epp))


plt.xlabel(r'$\lambda$ (\AA)', fontsize=20, labelpad=-3)
plt.ylabel(r'Norm Flux (erg s$^{-1}$ cm$^{-2}$ $\AA^{-1}$)', fontsize=16, labelpad=-3)
plt.legend(loc=0)
plt.xlim(4500, 12000)
plt.title("All Models - Encore: Targ. Ep " + str(nearest_epoch))
plt.savefig('plots/modelcomp_'+model_pdd+'_'+model_ddc+'_'+model_sch+'_'+str(nearest_epoch)+'.pdf')
plt.show()