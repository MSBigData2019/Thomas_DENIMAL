#!/usr/bin/env python3
#import numpy as np
import pandas as pd


url = '/data/dev/Thomas_DENIMAL/MDI720/Galton.txt'

df = pd.read_csv(url, sep='\t')


#Convert to inches
df[['Height', 'Father', 'Mother']] = 2.54*df[['Height', 'Father', 'Mother']]

#round to 0 decimals
df = df.round({'Father': 0, 'Mother': 0, 'Height': 0})

#Show head
print(df.head())

print('There is ' + df.isnull().sum().sum() + ' empty rows')
