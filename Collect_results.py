import numpy as np 
from astropy import table
from astropy.io import ascii
import matplotlib.pyplot as plt
import glob
import os 
import sys 
sys.path.insert(1,'/home/idoi/Dropbox/superfit/')
from get_metadata import *



path='/home/idoi/Dropbox/superfit/results_2018/*.csv'
file_list=glob.glob(path)

sample=ascii.read('/home/idoi/Dropbox/Objects/RCF/2018_test_metadata.ascii')
snid_sample=ascii.read('/home/idoi/Dropbox/Objects/RCF/ML_sample_snid_2018.csv')

sample=sample[sample['flag']==1]
cond=['P60' not in x for x in sample['name'] ]
sample=sample[cond]
sample.add_column(sample['ZTFname'].astype('S100'),name='SF_fit_1')
sample.add_column(0*sample['phase'].copy(),name='chi2_fit_1')
sample.add_column(0*sample['HGz'].copy()-1,name='zfit_1')
sample.add_column(0*sample['HGz'].copy()-1,name='zfit_2')
sample.add_column(sample['ZTFname'].astype('S100'),name='SF_fit_2')
sample.add_column(0*sample['phase'].copy(),name='chi2_fit_2')
sample.add_column(sample['ZTFname'].astype('S100'),name='c_snid')
sample.add_column(0*sample['phase'].copy(),name='c_rlap')
sample.add_column(0*sample['phase'].copy(),name='z_snid')


snid_sample['c_snid'][snid_sample['c_snid']=='II-norm']='II'
snid_sample['c_snid'][snid_sample['c_snid']=='Ia-norm']='Ia'
snid_sample['c_snid'][snid_sample['c_snid']=='Ia-csm']='Ia-CSM'
snid_sample['c_snid'][snid_sample['c_snid']=='Ia-03fg']='Ia-SC'
snid_sample['c_snid'][snid_sample['c_snid']=='Ib-norm']='Ib'
snid_sample['c_snid'][snid_sample['c_snid']=='Ic-norm']='Ic'
snid_sample['c_snid'][snid_sample['c_snid']=='Ic-SLSN']='SLSN-I'





for file in file_list:

    res=ascii.read(file)
    spec_name= res['OBJECT'][0]
    res.sort('CHI2/dof2')    
    short_name1,z1,chi2_1 = res['SN','Z','CHI2/dof2'][0]
    idx=short_name1.rfind('/')
    sn_type1=Type_dic[short_name1[0:idx]]
    cond=[spec_name[:-3] in x for x in sample['name']]
    sample['SF_fit_1'][cond] =  sn_type1
    sample['zfit_1'][cond] =  z1
    sample['chi2_fit_1'][cond] =  chi2_1
    if len(res)>1:
        short_name2,z2,chi2_2 = res['SN','Z','CHI2/dof2'][1]
        idx=short_name2.rfind('/')
        sn_type2=Type_dic[short_name2[0:idx]]
        sample['SF_fit_2'][cond] =  sn_type2
        sample['zfit_2'][cond] =  z2    
        sample['chi2_fit_2'][cond] =  chi2_2
    else: 
        sample['SF_fit_2'][cond] =  np.nan
        sample['zfit_2'][cond] =  np.nan
        sample['chi2_fit_2'][cond] =  np.nan
    try:
        cond2=[spec_name[:-3] in x for x in snid_sample['Version']]
        sample['c_snid'][cond] = snid_sample['c_snid'][cond2]
        sample['z_snid'][cond] = snid_sample['z_snid'][cond2]
        sample['c_rlap'][cond] = snid_sample['c_rlap'][cond2]
    except:
        cond2=[spec_name[:-5] in x for x in snid_sample['Version']]
        if np.sum(cond2)==1:
            sample['c_snid'][cond] = snid_sample['c_snid'][cond2]
            sample['z_snid'][cond] = snid_sample['z_snid'][cond2]
            sample['c_rlap'][cond] = snid_sample['c_rlap'][cond2]
        elif np.sum(cond2)>1:
            best = snid_sample['c_rlap'][cond2]==np.max(snid_sample['c_rlap'][cond2])
            sample['c_snid'][cond] = snid_sample['c_snid'][cond2][best]
            sample['z_snid'][cond] = snid_sample['z_snid'][cond2][best]
            sample['c_rlap'][cond] = snid_sample['c_rlap'][cond2][best] 






sample['SF_fit_2'][sample['ZTFname']==sample['SF_fit_2']]=np.nan
sample['SF_fit_1'][sample['ZTFname']==sample['SF_fit_1']]=np.nan
sample=sample[sample['SF_fit_1']!='nan']
#sample2=sample.copy()
#for sn in np.unique(sample['ZTFname']):
#    cond = sample['ZTFname']==sn
#    sample.remove_rows(np.argwhere(cond)[0:-1])
#








sample['classification'][sample['classification']=='II-87A']='II'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia-norm']='Ia'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia-norm']='Ia'
sample['SF_fit_1'][sample['SF_fit_1']=='II-flash']='II'
sample['SF_fit_2'][sample['SF_fit_2']=='II-flash']='II'
sample['SF_fit_1'][sample['SF_fit_1']=='SLSN-IIn']='SLSN-II'
sample['SF_fit_2'][sample['SF_fit_2']=='SLSN-IIn']='SLSN-II'
sample['SF_fit_1'][sample['SF_fit_1']=='SLSN-Ib']='SLSN-I'
sample['SF_fit_2'][sample['SF_fit_2']=='SLSN-Ib']='SLSN-I'
sample['SF_fit_1'][sample['SF_fit_1']=='\"super chandra\"']='Ia-SC'
sample['SF_fit_2'][sample['SF_fit_2']=='\"super chandra\"']='Ia-SC'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia 91T-like']='Ia-91T'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia 91T-like']='Ia-91T'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia 91bg-like']='Ia-91bg'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia 91bg-like']='Ia-91bg'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia-02cx like']='Ia-02cx'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia-02cx like']='Ia-02cx'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia 99aa-like']='Ia'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia 99aa-like']='Ia'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia-pec']='Ia'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia-pec']='Ia'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia-rapid']='Ia'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia-rapid']='Ia'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia 02es-like']='Ia'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia 02es-like']='Ia'
sample['SF_fit_1'][sample['SF_fit_1']=='Ia-CSM-(ambigious)']='ambigious'
sample['SF_fit_2'][sample['SF_fit_2']=='Ia-CSM-(ambigious)']='ambigious'
sample['SF_fit_1'][sample['SF_fit_1']=='Ca-Ia']='Ia'
sample['SF_fit_2'][sample['SF_fit_2']=='Ca-Ia']='Ia'
sample['SF_fit_1'][sample['SF_fit_1']=='Ca-Ibc']='Ib/c'
sample['SF_fit_2'][sample['SF_fit_2']=='Ca-Ibc']='Ib/c'





def get_SN(SN_name,table=sample):
    cond=[SN_name in x for x in sample['ZTFname']]
    return table[cond]

def get_accuracy(sample,SN_type, exact=True, quality_cut='None', col='SF_fit_1'):
    if quality_cut!='None':
        sample=sample[quality_cut]

    if bool(exact)==True:
        real_true=sample['classification']==SN_type
        if col!='all':
            class_true=sample[col]==SN_type
        elif col=='all':
            class_true=(sample['SF_fit_1']==SN_type)&(sample['c_snid']==SN_type)
    else:
        real_true=np.array([SN_type in x for x in sample['classification']])
        if col!='all':
            class_true=np.array([SN_type in x for x in sample[col]])

        elif col=='all':
            class_true=np.array([SN_type in x for x in sample['SF_fit_1']]) & np.array([SN_type in x for x in sample['c_snid']])

    TP = (class_true ) & (real_true)
    FP = (class_true ) & (~real_true)
    FN = (~class_true) & (real_true)
    TN = (~class_true) & (~real_true)
    P= TP|FN
    N= FP|TN

    TPR = np.sum(TP)/np.sum(P)
    TNR = np.sum(TN)/np.sum(N)
    FPR = np.sum(FP)/np.sum(N)
    FNR = np.sum(FN)/np.sum(P)


    return (TPR ,FPR, TNR, FNR), (np.sum(TP), np.sum(FP), np.sum(TN), np.sum(FN))



def get_full_accuray(sample,exact=True,quality_cut='None', col='SF_fit_1'):
    if exact:
        class_list=np.unique(sample['SF_fit_1'])
    else: 
        class_list=[]
    _,N = get_accuracy(sample,SN_type, exact=exact, quality_cut=quality_cut, col=col)
    NTP,NFP,NTN,NFN=N

    

#iqr_chi1=np.nanpercentile(sample['chi2_fit_1'], [75 ,25])
#iqr_chi1=np.abs(iqr_chi1[0]-iqr_chi1[1])
#quality=sample['chi2_fit_1']<(np.nanmedian(sample['chi2_fit_1'])+3*iqr_chi1)
#get_accuracy(sample,'Ia', exact=False,quality_cut=quality, col='SF_fit_1') 
#


print('All classifications:')





print('Ia')
accuracy,N=get_accuracy(sample,'Ia', exact=False, col='SF_fit_1') 
print('Superfit:')
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
accuracy,N=get_accuracy(sample,'Ia', exact=False, col='c_snid') 
print('SNid:')
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'Ia', exact=False, col='all')
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))

print('II-all')
print('Superfit:')

accuracy,N=get_accuracy(sample,'II', exact=False, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))

print('SNid:')

accuracy,N=get_accuracy(sample,'II', exact=False, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'II', exact=False, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))



print('II-norm')
print('Superfit:')

accuracy,N=get_accuracy(sample,'II', exact=True, col='SF_fit_1')
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'II', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'II', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))


print('IIn')
print('Superfit:')

accuracy,N=get_accuracy(sample,'IIn', exact=True, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'IIn', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'IIn', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))



print('IIb')
print('Superfit:')

accuracy,N=get_accuracy(sample,'IIb', exact=True, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'IIb', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'IIb', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))



print('Ib')
print('Superfit:')

accuracy,N=get_accuracy(sample,'Ib', exact=True, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'Ib', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'Ib', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))




print('Ic')
print('Superfit:')

accuracy,N=get_accuracy(sample,'Ic', exact=True, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'Ic', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'Ic', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))



print('SLSN-I')
print('Superfit:')

accuracy,N=get_accuracy(sample,'SLSN-I', exact=True, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'SLSN-I', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'SLSN-I', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))


print('SLSN-II')
print('Superfit:')

accuracy,N=get_accuracy(sample,'SLSN-II', exact=True, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'SLSN-II', exact=True, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'SLSN-II', exact=True, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))





print('SLSN-all')
print('Superfit:')

accuracy,N=get_accuracy(sample,'SLSN', exact=False, col='SF_fit_1') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('SNid:')

accuracy,N=get_accuracy(sample,'SLSN', exact=False, col='c_snid') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))
print('both:')

accuracy,N=get_accuracy(sample,'SLSN', exact=False, col='all') 
print('TPR={0:.2f} (N={1}) ,FPR={2:.2f} (N={3}), TNR={4:.2f} (N={5}), FNR={6:.2f} (N={7})'.format(accuracy[0],N[0],accuracy[1],N[1],accuracy[2],N[2],accuracy[3],N[3]))








plt.figure()
#plt.plot(sample['redshift'],sample['zfit_1']-sample['redshift'],'*')
plt.plot(np.round(sample['redshift'],2),sample['zfit_1'],'.r')
#plt.plot(np.round(sample['redshift'],2),sample['zfit_1']-sample['redshift'],'.r')

plt.show()
