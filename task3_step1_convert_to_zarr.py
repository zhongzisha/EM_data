
import os
import tifffile
import zarr
import numpy as np


def save_tif_to_zarr(tif_filename, zarr_filename):

    if not os.path.exists(tif_filename):
        print(f'{tif_filename} not existed.')
        return

    if os.path.exists(zarr_filename):
        print(f'{zarr_filename} existed.')
        return

    dirname = os.path.dirname(zarr_filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname, exist_ok=True)

    image_array = []
    with tifffile.TiffFile(tif_filename) as tif:
        for i in range(len(tif.pages)):

            image_data = tif.pages[i].asarray()
            # image_data[image_data>2048] = 2048
            # image_data = (255*(image_data.astype(np.float32)/2048)).astype(np.uint8)
            # cv2.imwrite(os.path.join(save_root, f'dapi_{i}.jpg'), cv2.resize(image_data, dsize=None, fx=0.25, fy=0.25))
            # time.sleep(1)
            # break
            image_array.append(image_data)
    image_array = np.stack(image_array)

    zarr_array = zarr.open(zarr_filename, mode='w', shape=image_array.shape, dtype=image_array.dtype)
    zarr_array[:] = image_array


def save_dm3_to_zarr():

    import dm3_lib as dm3
    import glob
    filenames = sorted(glob.glob('data/EMPIAR-11759/data/*.dm3'))
    zarr_filename = 'data/EMPIAR-11759.zarr'
    if os.path.exists(zarr_filename):
        print(f'{zarr_filename} existed.')
        return

    image_array = []
    for f in filenames:
        dm3f = dm3.DM3(f)
        print(dm3f.width, dm3f.height, dm3f.pxsize)
        image_array.append(dm3f.imagedata)
    image_array = np.stack(image_array)

    zarr_array = zarr.open(zarr_filename, mode='w', shape=image_array.shape, dtype=image_array.dtype)
    zarr_array[:] = image_array



def main():

    save_tif_to_zarr('data/data-em/volumedata.tif', 'data/data_em.zarr')

    save_tif_to_zarr(
        'data/EMBL/Miron_FIB-SEM/Miron_FIB-SEM_processed/Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy.tif', 
        'data/EMBL_Miron_FIB-SEM.zarr')

    print('Done')

if __name__ == '__main__':
    main()
    save_dm3_to_zarr()
