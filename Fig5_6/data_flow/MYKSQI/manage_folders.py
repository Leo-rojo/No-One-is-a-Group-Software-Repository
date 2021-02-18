import pandas as pd
import numpy as np
import os
data = pd.read_csv("datavideo.csv")
for col in data.columns[8:40]:
    df = data.assign(mos=data[col])
    a = 'C:\\Users\\leona\\Desktop\\usuful_program\\ksqi-master_original\\'
    b = a + str(col) +'2\\'
    os.makedirs(b)
    df.to_csv(b + 'data.csv', index=False)