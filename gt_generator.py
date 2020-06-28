#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## data process module: read next image, and process them to fit the cornernet model
#---read image
import os
import pandas as pd
import numpy as np
import scipy.io as scio

def wash_tracks(data):
    new_data = {} # save 40 long tracks.
    label_idx = 1
    original_idx = {}
    for i in range(1, data.id.max()):
        data_frame = data[data.id==i]
        x_ = data_frame['Y'].tolist()
        if len(x_)>100:
            new_data[label_idx] = data_frame
            original_idx[label_idx] = i
            label_idx = label_idx + 1
            
    return new_data, label_idx, original_idx

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


file = '20091021_truth_rset0_frames0100-0611.xls'
tracks = pd.read_excel(os.path.join(file))
tracks, max_ids, original_idx = write_tracks(tracks)
print('total track num is', max_ids)



