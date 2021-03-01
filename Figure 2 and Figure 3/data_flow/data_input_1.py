import openpyxl
import csv
import os
import glob

wb1 = openpyxl.load_workbook('./data/datain/data.xlsx')
ws1 = wb1.active
usercols=['I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN']
usnr=0
for col in usercols:
    usnr+=1
    for src, dst in zip(ws1[col],ws1['B']):
        dst.value = src.value
    ws1.cell(row=1,column=2).value = 'mos'

    with open('./data/dataout/user'+str(usnr)+'hdtv'+'.csv', 'w',newline='') as f:
        c = csv.writer(f)
        for r in ws1.rows:
            print(r)
            c.writerow([cell.value for cell in r])

# remove useless column
os.chdir('./data/dataout')
FileList = glob.glob('*.csv')
contafile=0
for file in FileList:
    contafile+=1
    with open(file, "r") as source:
        rdr = csv.reader(source)
        with open(file.replace('.csv','')+'_ready.csv', "w",newline='') as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow((r[0], r[1], r[2] ,r[3], r[4],r[5], r[6], r[7] ))

