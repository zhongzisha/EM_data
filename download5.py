# https://tinyurl.com/hemibrain-ng (download only a random 1000x1000x1000 pixel crop region)

# the following code is modified from https://gist.github.com/jbms/10b7a91c8b2f8ecbf30a869a1c50defb

import os
# Ensure tensorstore does not attempt to use GCE credentials
os.environ['GCE_METADATA_ROOT'] = 'metadata.google.internal.invalid'
import tensorstore as ts
import numpy as np
import matplotlib.pyplot as plt
import zarr

context = ts.Context({'cache_pool': {'total_bytes_limit': 1000000008}})

em_8nm = ts.open({
    'driver': 'neuroglancer_precomputed',
    'kvstore': 'gs://neuroglancer-janelia-flyem-hemibrain/emdata/clahe_yz/jpeg/'},
    read=True, context=context).result()[ts.d['channel'][0]]

shape = em_8nm.shape  # get the image size

## get a crop region 1000x1000x1000 around the center

patch_size = 1000
radius = patch_size // 2

# get the crop center
x = shape[0]//2
y = shape[1]//2
z = shape[2]//2

# crop the region
img_cutout_8nm = em_8nm[x-radius:x+radius, y-radius:y+radius, z-radius:z+radius].read().result()

print(type(img_cutout_8nm))  # numpy.ndarray
print(img_cutout_8nm.dtype)  # uint8
print(img_cutout_8nm.shape)  # 128x128x128
print(img_cutout_8nm.min())  # 0
print(img_cutout_8nm.max())  # 255

# save to zarr dataset
zarr_filename = 'data/hemibrain-ng_1000x1000x1000.zarr'
if not os.path.exists(zarr_filename):
    zarr_array = zarr.open(zarr_filename, mode='w', shape=img_cutout_8nm.shape, dtype=img_cutout_8nm.dtype)
    zarr_array[:] = img_cutout_8nm



## crop a 128x128x128 region from randomly position (x,y,z)

patch_size = 128  # cube size
radius = patch_size // 2

# get the crop center
x = np.random.randint(low=radius, high=shape[0]-radius)
y = np.random.randint(low=radius, high=shape[1]-radius)
z = np.random.randint(low=radius, high=shape[2]-radius)

# crop the region
img_cutout_8nm = em_8nm[x-radius:x+radius, y-radius:y+radius, z-radius:z+radius].read().result()

print(type(img_cutout_8nm))  # numpy.ndarray
print(img_cutout_8nm.dtype)  # uint8
print(img_cutout_8nm.shape)  # 128x128x128
print(img_cutout_8nm.min())  # 0
print(img_cutout_8nm.max())  # 255







