#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## data process module: read next image, and process them to fit the cornernet model
#---read image
import os
import pandas as pd
import numpy as np
import scipy.io as scio

import matplotlib.pyplot as plt

rows = ['original_ids', 'new_ids', 'frame_num','occlusion', 'background change', 'motion change', 'distractors']

def write_tracks(data):
    new_data = {} # save 40 long tracks.
    label_idx = 1
    original_idx = {}
    for i in range(1, data.id.max()):
        data_frame = data[data.id==i]
        x_ = data_frame['Y'].tolist()
        if len(x_)>100:
            le = len(x_)
            new_data[label_idx] = data_frame
            original_idx[label_idx] = i
            or_ids = [i]*le
            new_ids = [label_idx]*le
            frame_num = data_frame['FRAME_NUMBER'].tolist()
            df = pd.DataFrame({rows[0]:or_ids,rows[1]:new_ids,rows[2]:frame_num,
                               rows[3]:[0]*le,rows[4]:[0]*le,rows[5]:[0]*le,
                               rows[6]:[0]*le})
            excel_name = 'gt_track'+str(label_idx)+'.xls'
            df = df[rows]
            df.to_excel(excel_name)
            print('done!',excel_name)
            label_idx = label_idx + 1
    return new_data, label_idx, original_idx

scores = []
ocs, bgs, mos, diss = [], [], [], []
for i in range(1,184):    
    file = 'gt_track'+str(i)+'.xls'
    tracks = pd.read_excel(os.path.join(file))
    oc = sum(tracks['occlusion'].tolist())
    bg = sum(tracks['background change'].tolist())
    mo = sum(tracks['motion change'].tolist())
    dis = sum(tracks['distractors'].tolist())
    score = oc + bg + 0.5*mo + 0.5+dis
    ocs.append(oc)
    bgs.append(bg)
    mos.append(mo)
    diss.append(dis)
    scores.append(score)

scores = np.array(scores)
ocs = np.array(ocs)
bgs = np.array(bgs)
mos = np.array(mos)
diss = np.array(diss)

rank1 = np.argsort(scores)
scores = scores[rank1]
ocs = ocs[rank1]
bgs = bgs[rank1]
mos = mos[rank1]
diss = diss[rank1]

'''fig 1'''
plt.bar(range(len(scores)), scores)
plt.grid('On')
plt.xlabel('Sample number')
plt.ylabel('Difficulty score')
plt.savefig('fig1.png', dpi=500)
plt.show()

'''fig 2'''

oc1,oc2,oc3 = np.mean(ocs[:100]),np.mean(ocs[100:150]),np.mean(ocs[150:])
bg1,bg2,bg3 = np.mean(bgs[:100]),np.mean(bgs[100:150]),np.mean(bgs[150:])
bg1,bg2,bg3 = np.mean(bgs[:100]),np.mean(bgs[100:150]),np.mean(bgs[150:])

size = 3
x = np.arange(size)
a = [np.mean(ocs[:100]),np.mean(ocs[100:150]),np.mean(ocs[150:])]
b = [np.mean(bgs[:100]),np.mean(bgs[100:150]),np.mean(bgs[150:])]
c = [np.mean(mos[:100]),np.mean(mos[100:150]),np.mean(mos[150:])]
d = [np.mean(diss[:100]),np.mean(diss[100:150]),np.mean(diss[150:])]

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / 2
labels = ['Easy group', 'Medium group', 'Hard group']

plt.bar(x, a,  width=width, label='Occlusion')
plt.bar(x + width, b, width=width, label='Enviroment changes')
plt.bar(x + 2 * width, c, width=width, label='Motion changes',tick_label=labels)
plt.bar(x + 3 * width, d, width=width, label='Distractors')

plt.grid('On')
plt.ylabel('Mean frames')
plt.legend()
plt.savefig('fig2.png', dpi=500)
plt.show()