import os
import glob
from shutil import copyfile

datain='.\\data\\dataout\\'
dataout='.\\MYKSQI\\data\\WaterlooSQoE-IV\\'
cwd = os.getcwd()
print(cwd)
os.chdir('.\\data\\dataout')
cwd = os.getcwd()
print(cwd)
FileList = glob.glob('*.csv')
FileList = [s for s in FileList if 'ready' in s]
os.chdir('..')
os.chdir('..')
print(os.getcwd())
contafile=0
for file in FileList:
    contafile+=1
    copyfile(datain+file, dataout+'data.csv')

    #runna file con args
    os.chdir('.\\MYKSQI')
    os.system('python .\\main.py --set DATASET WaterlooSQoE-IV INPUT_DIR data/WaterlooSQoE-IV MODEL FTW:Mok2011QoE:Liu2012QoE:Xue2014QoE:Yin2015QoE:Spiteri2016QoE:Bentaleb2016QoE:SQI:P1203:VideoATLAS:KSQI')
    #os.system('python C:\\Users\\leona\\Desktop\\MYKSQI\\main.py --set DATASET WaterlooSQoE-IV INPUT_DIR data/WaterlooSQoE-IV MODEL Mok2011QoE')
    os.chdir('..')
    copyfile('.\\MYKSQI/results/WaterlooSQoE-IV/performance.csv','.\\data/resultsmixture\\'+'performance_'+file)
    #copyfile('C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\MYKSQI/results/WaterlooSQoE-IV/scores.csv','C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\data/resultsmixture\\' +'scores_'+file)