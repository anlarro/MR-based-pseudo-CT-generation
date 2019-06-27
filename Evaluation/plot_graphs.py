import os
import numpy as np
import pandas as pd

import plotly.io as pio
import plotly as py
import plotly.graph_objs as go
from plotly.offline import *

import scipy.stats
import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols

py.io.orca.config.executable = '/home/andres/anaconda3/envs/myenv/lib/orca_app/orca'
py.io.orca.config.save()

#fold1
# M1 = np.array([77.80, 86.52, 114.15, 108.12, 105.86])
# M2 = np.array([99.33, 103.24, 129.29, 124.14, 124.64])
# M3 = np.array([91.86, 99.32, 114.73, 109.26, 104.38])
# M4 = np.array([110.95, 110.95, 129.54, 124.97, 123.81])
# M5 = np.array([78.16, 87.34, 107.45, 105.40, 100.07])
# M6 = np.array([88.10, 101.55, 122.09, 126.98, 117.52])
# M7 = np.array([83.33, 86.36, 112.95, 98.84, 95.36])
# M8 = np.array([85.81, 95.48, 112.74, 100.39, 107.95])
# M9 = np.array([112.44, 92.35, 118.93, 112.34, 126.67])
uclT1 = np.array([240.26, 187.50, 147.57, 154.59, 149.12])
uclT2 = np.array([255.75, 223.07, 147.43, 182.65, 162.17])

#CV
M1 = np.array([120.78,98.99,77.80,127.56,112.06,86.52,116.69,125.32,114.15,110.56,108.12389,101.00203,105.85848])
M2 = np.array([154.10,113.46,99.33,165.54,105.83,103.24,136.99,139.28,129.29,127.44,124.142204,116.873535,124.63811])
M3 = np.array([114.41,104.74,91.86,106.94,99.32,99.32,118.88,134.75,114.73,110.44,109.26097,110.19497,104.37529])
M4 = np.array([151.58,135.48,110.95,129.56,124.64,110.95,143.73,163.20,129.54,128.14,124.97441,126.70609,123.80875])
M5 = np.array([99.75,108.35,78.16,112.30,102.04,87.34,96.88,118.16,107.45,99.60,105.39842,96.87295,100.074165])
M6 = np.array([136.12,122.43,88.10,155.85,110.80,101.55,118.12,149.40,122.09,126.87,126.979355,114.85343,117.5234])
M7 = np.array([118.00,99.62,83.33,111.76,89.97,86.36,116.83,115.67,112.95,111.23,98.84388,105.64942,95.364716])
M8 = np.array([111.72,103.69,85.81,105.06,107.08,95.48,97.13,124.96,112.74,110.42,100.38544,110.92906,107.94967])
M9 = np.array([116.28,100.66,112.28,124.97,95.14,87.73,107.18,137.77,119.89,109.06,111.880264,105.32819,130.78232])

mris = ['mrT1', 'mrT1', 'mrT1', 'mrT1', 'mrT1',
        'mrT2', 'mrT2', 'mrT2', 'mrT2', 'mrT2',
        'mrT1/mrT2','mrT1/mrT2','mrT1/mrT2','mrT1/mrT2','mrT1/mrT2']

nnets = ['Vnet', 'Vnet', 'Vnet', 'Vnet', 'Vnet',
        'HighRes3dNet', 'HighRes3dNet', 'HighRes3dNet', 'HighRes3dNet', 'HighRes3dNet',
        'ScaleNet','ScaleNet','ScaleNet','ScaleNet','ScaleNet']

vnet = go.Box(
    y=np.concatenate((M2,M4,M6)),
    x=mris,
    name='Vnet',
    marker=dict(
        color='#3D9970'
    )
)
highres = go.Box(
    y=np.concatenate((M1,M3,M5)),
    x=mris,
    name='HighRes3dNet',
    marker=dict(
        color='#FF4136'
    )
)

scalenet = go.Box(
    y=np.concatenate((M8,M9,M7)),
    x=mris,
    name='ScaleNet',
    marker=dict(
        color='#1eafed'
    )
)

############
mrT1 = go.Box(
    y=np.concatenate((M2,M1,M8)),
    x=nnets,
    name='mrT1',
    marker=dict(
        color= '#ff7f0e'
    )
)
mrT2 = go.Box(
    y=np.concatenate((M4,M3,M9)),
    x=nnets,
    name='mrT2',
    marker=dict(
        # color='#FF4136'
        color='#9467bd'
    )
)

mrT1mrT2 = go.Box(
    y=np.concatenate((M6,M5,M7)),
    x=nnets,
    name='mrT1/mrT2',
    marker=dict(
        # color='#FF851B',
        color='#8c564b'
    )
)

data1 = [vnet, highres, scalenet]
layout = go.Layout(
    yaxis=dict(
        title='Mean Absolute Error',
        zeroline=False
    ),
    boxmode='group',
    legend=dict(x=0, y=1.15,orientation="h"),
    font=dict(size=20),
)
fig1 = go.Figure(data=data1, layout=layout)
py.offline.plot(fig1, filename='boxplot1.html')
pio.write_image(fig1, '/home/andres/Dropbox/Papers/EMBC 2019/images/boxplot1.svg')

data2 = [mrT1, mrT2, mrT1mrT2]
layout = go.Layout(
    yaxis=dict(
        title='Mean Absolute Error',
        zeroline=False
    ),
    boxmode='group',
    legend=dict(x=0, y=1.15,orientation="h"),
    font=dict(size=20),
)
fig2 = go.Figure(data=data2, layout=layout)
py.offline.plot(fig2, filename='boxplot2.html')
pio.write_image(fig2, '/home/andres/Dropbox/Papers/EMBC 2019/images/boxplot2.svg')

#########
#Calculate p-values
#Between nnets
print('M2 vs M1: p-value =', (0.05/3) > scipy.stats.ttest_ind(M2, M1)[1],scipy.stats.ttest_ind(M2, M1)[1])
print('M2 vs M8: p-value =', (0.05/3) > scipy.stats.ttest_ind(M2, M8)[1],scipy.stats.ttest_ind(M2, M8)[1])
print('M1 vs M8: p-value =', (0.05/3) > scipy.stats.ttest_ind(M1, M8)[1],scipy.stats.ttest_ind(M1, M8)[1])

print('M4 vs M3: p-value =', (0.05/3) > scipy.stats.ttest_ind(M4, M3)[1],scipy.stats.ttest_ind(M4, M3)[1])
print('M4 vs M9: p-value =', (0.05/3) > scipy.stats.ttest_ind(M4, M9)[1],scipy.stats.ttest_ind(M4, M9)[1])
print('M3 vs M9: p-value =', (0.05/3) > scipy.stats.ttest_ind(M3, M9)[1],scipy.stats.ttest_ind(M3, M9)[1])

print('M6 vs M5: p-value =', (0.05/3) > scipy.stats.ttest_ind(M6, M5)[1],scipy.stats.ttest_ind(M6, M5)[1])
print('M6 vs M7: p-value =', (0.05/3) > scipy.stats.ttest_ind(M6, M7)[1],scipy.stats.ttest_ind(M6, M7)[1])
print('M5 vs M7: p-value =', (0.05/3) > scipy.stats.ttest_ind(M5, M7)[1],scipy.stats.ttest_ind(M5, M7)[1])


#Between MRI sequences
print('M2 vs M4: p-value =', (0.05/3) > scipy.stats.ttest_ind(M2, M4)[1],scipy.stats.ttest_ind(M2, M4)[1])
print('M2 vs M6: p-value =', (0.05/3) > scipy.stats.ttest_ind(M2, M6)[1],scipy.stats.ttest_ind(M2, M6)[1])
print('M4 vs M6: p-value =', (0.05/3) > scipy.stats.ttest_ind(M4, M6)[1],scipy.stats.ttest_ind(M4, M6)[1])

print('M1 vs M3: p-value =', (0.05/3) > scipy.stats.ttest_ind(M1, M3)[1],scipy.stats.ttest_ind(M1, M3)[1])
print('M1 vs M5: p-value =', (0.05/3) > scipy.stats.ttest_ind(M1, M5)[1],scipy.stats.ttest_ind(M1, M5)[1])
print('M3 vs M5: p-value =', (0.05/3) > scipy.stats.ttest_ind(M3, M5)[1],scipy.stats.ttest_ind(M3, M5)[1])

print('M8 vs M9: p-value =', (0.05/3) > scipy.stats.ttest_ind(M8, M9)[1],scipy.stats.ttest_ind(M8, M9)[1])
print('M8 vs M7: p-value =', (0.05/3) > scipy.stats.ttest_ind(M8, M7)[1],scipy.stats.ttest_ind(M8, M7)[1])
print('M9 vs M7: p-value =', (0.05/3) > scipy.stats.ttest_ind(M9, M7)[1],scipy.stats.ttest_ind(M9, M7)[1])

#Compared to atlas
print('p-value =', (0.05) > scipy.stats.ttest_ind(M1, uclT1)[1],scipy.stats.ttest_ind(M1, uclT1)[1])
print('p-value =', (0.05) > scipy.stats.ttest_ind(M2, uclT1)[1],scipy.stats.ttest_ind(M2, uclT1)[1])
print('p-value =', (0.05) > scipy.stats.ttest_ind(M8, uclT1)[1],scipy.stats.ttest_ind(M8, uclT1)[1])

print('p-value =', (0.05) > scipy.stats.ttest_ind(M3, uclT2)[1],scipy.stats.ttest_ind(M3, uclT2)[1])
print('p-value =', (0.05) > scipy.stats.ttest_ind(M4, uclT2)[1],scipy.stats.ttest_ind(M4, uclT2)[1])
print('p-value =', (0.05) > scipy.stats.ttest_ind(M9, uclT2)[1],scipy.stats.ttest_ind(M9, uclT2)[1])

formula = 'len ~ C(supp) + C(dose) + C(supp):C(dose)'
model = ols(formula, data).fit()
aov_table = statsmodels.stats.anova.anova_lm(model, typ=2)
print(aov_table)