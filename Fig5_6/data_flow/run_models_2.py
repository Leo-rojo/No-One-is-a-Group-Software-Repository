import os
import glob
from shutil import copyfile

datain='C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\data\\dataout\\'
dataout='C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\MYKSQI\\data\\WaterlooSQoE-IV\\'
cwd = os.getcwd()
print(cwd)
os.chdir('C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\data\\dataout')
cwd = os.getcwd()
print(cwd)
FileList = glob.glob('*.csv')
FileList = [s for s in FileList if 'ready' in s]
os.chdir('C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow')
contafile=0
for file in FileList:
    contafile+=1
    copyfile(datain+file, dataout+'data.csv')

    #runna file con args
    os.chdir('C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\MYKSQI')
    os.system('python C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\MYKSQI\\main.py --set DATASET WaterlooSQoE-IV INPUT_DIR data/WaterlooSQoE-IV MODEL FTW:Mok2011QoE:Liu2012QoE:Xue2014QoE:Yin2015QoE:Spiteri2016QoE:Bentaleb2016QoE:SQI:P1203:VideoATLAS:KSQI')
    #os.system('python C:\\Users\\leona\\Desktop\\MYKSQI\\main.py --set DATASET WaterlooSQoE-IV INPUT_DIR data/WaterlooSQoE-IV MODEL Mok2011QoE')
    copyfile('C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\MYKSQI/results/WaterlooSQoE-IV/performance.csv','C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\data/resultsmixture\\'+'performance_'+file)
    #copyfile('C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\MYKSQI/results/WaterlooSQoE-IV/scores.csv','C:\\Users\\leona\\Desktop\\no-one-is-a-group\\Fig5_6\\data_flow\\data/resultsmixture\\' +'scores_'+file)