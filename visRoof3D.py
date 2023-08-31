import os

import ipdb
from pycocotools.mask import frPyObjects, decode
import json
import rasterio as rio
import matplotlib.pyplot as plt
import numpy as np


basedir = '/path/to/ROOF3D'
fold = 'train' # 'val'
src = 'rgb' # 'dsm'
anno_name = 'plane' # 'sec'

ann_file = os.path.join(basedir,fold,'annotation_'+anno_name+'.json')

with open(ann_file,'r') as f:
  annotations = json.load(f)

annos = annotations["annotations"]

by_image_id = {}
for item in annos:
    image_id = item['image_id']
    segmentation = item['segmentation']
    
    if image_id not in by_image_id:
        by_image_id[image_id] = []
    
    by_image_id[image_id] += [segmentation]

for image_id, segmentations in by_image_id.items():

    img_path = os.path.join(basedir,fold,src,str(image_id)+'.tif')
    with rio.open(img_path,'r') as image: 
        img = image.read()
    
    if img.shape[0] == 1:
        img = img.repeat(3,0).transpose(1,2,0)
    elif img.shape[0] == 3:
        img = img.transpose(1,2,0)
    
    img_norm = img / 255
     
    masks = []
    for seg in segmentations:
        for rle in seg:
            rle_ = frPyObjects(rle, rle.get('size')[0], rle.get('size')[1])
            mask = decode(rle_)
            masks += [mask]
    
    colors = np.random.rand(100,3)
    np.random.shuffle(colors)
    
    instances = np.zeros((mask.shape[0],mask.shape[1],3))
    for idx, mask in enumerate(masks):
        color = colors[idx % len(colors)]
        mask_expanded = np.expand_dims(mask,2).repeat(3,2)
        instances += mask_expanded * color
    
    inst_mask = instances.sum(2)
    inst_mask = np.where(inst_mask > 0, 1, 0)
        
    for i in range(3): img_norm[:,:,i] = (1 - inst_mask) * img_norm[:,:,i] + inst_mask * instances[:,:,i]
    
    plt.imshow(img_norm)
    plt.show()
