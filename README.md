

# Task 1

1. Install the Globus and setup the account for local storage. Install the Google-Cloud-SDK and make sure to have the access to Google Cloud Storage. 

2. Install the Python 3.12 and the related Python libraries:
```
pip install globus-cli zarr tensorstore
pip install git+https://github.com/piraynal/pyDM3reader.git  # to read DM3 images
```

3. Signin the Glubus.
```
globus login
```

4. Run the following commands.
```
bash download1.sh
bash download2.sh
bash download3.sh
bash download4.sh
python download5.py
```

5. The five datasets will be stored in the `data` directory, like this.
```
data
├── data-em
├── EMBL
├── EMPIAR-11759
├── hemibrain-ng_1000x1000x1000.zarr
└── jrc_mus-nacc-2
```

# Task 2
First, I collected the metadata from the webpage of each dataset and listed it in a Google Sheet ([link](https://docs.google.com/spreadsheets/d/1sRJtdbJOCdzBCWieZm3p8rwkODft3VM6iDRl2EIZRKo/edit?usp=drive_link)). After that, I identified the common metadata fields across the datasets and determined which ones were most important. Finally, I summarized this key information in a single table, as follows (also in [CSV](./consolidated_meta.csv) format).

For `dataset2`, there is a discrepancy between the image dimensions reported on the dataset webpage and the actual dimensions found in the image data.
The true width and height of the image data have been verified and are correctly listed in the table provided. 

For `dataset5`, the FlyEM hemibrain data, the pixel resolution reported in the original publication is 4 nm. However, the version available via the neuroglancer_precomputed format on Google Cloud has a pixel resolution of 8 nm.
This discrepancy suggests that the publicly accessible dataset may be a resampled version of the original high-resolution data.
If the original 4 nm data is required for your analysis or project, it is advisable to contact the data owner or the FlyEM team for confirmation and access.

| name     | url                                                                        |   depth |   height |   width | pixel_type   | pixel_size_in_nm   | experiment_type   | species      | organ             | publication_url                                             |
|:---------|:---------------------------------------------------------------------------|--------:|---------:|--------:|:-------------|:-------------------|:------------------|:-------------|:------------------|:------------------------------------------------------------|
| dataset1 | https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740 |     184 |      775 |    1121 | uint8        | [50, 50, 50]       | FIB-SEM           | Homo sapiens | chromatin         | https://www.science.org/doi/10.1126/sciadv.aba8811          |
| dataset2 | https://www.ebi.ac.uk/empiar/EMPIAR-11759/                                 |      16 |     5500 |    5496 | uint8        | [80, 80, 80]       | SBF-SEM           | zebrafish    | eye               | https://doi.org/10.6019/EMPIAR-11759                        |
| dataset3 | https://www.epfl.ch/labs/cvlab/data/data-em/                               |    1065 |     1536 |    2048 | uint8        | [5, 5, 5]          | EM                | unknown      | mitochondria      | https://ieeexplore.ieee.org/document/6619103                |
| dataset4 | https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2                  |     564 |     2520 |    2596 | int16        | [2.96, 4, 4]       | FIB-SEM           | Mouse        | nucleus accumbens | https://www.nature.com/articles/s41586-021-03992-4          |
| dataset5 | https://www.janelia.org/project-team/flyem/hemibrain                       |    1000 |     1000 |    1000 | uint8        | [8, 8, 8]          | FIB-SEM           | fly          | brain             | https://www.biorxiv.org/content/10.1101/2024.04.21.590464v1 |

# Task 3

The **Zarr** library (https://zarr.dev/) provides high-throughput, distributed I/O for multi-scale, n-dimensional images across various storage systems. It supports concurrent reading and writing of arrays from multiple threads or processes and organizes arrays into hierarchies using annotatable groups. These features make it well-suited to the requirements. 

To access each image in a block-wise manner, we first convert the datasets into Zarr format. Then we provide a demo for 3-D CNN training in PyTorch. 

**Step 1**: Convert the datasets into Zarr.
```
python task3_step1_convert_to_zarr.py
```
The generated Zarr dataset are saved in the `data` directory, like this:
```
data
├── data_em.zarr
├── data-em
├── EMBL
├── EMBL_Miron_FIB-SEM.zarr
├── EMPIAR-11759
├── EMPIAR-11759.zarr
├── hemibrain-ng_1000x1000x1000.zarr
└── jrc_mus-nacc-2
```

**Step 2**: Train a 3-D CNN on the Zarr datasets.
```
python task3_step2.py
```
The outputs will be like this:
```
(venv) NCI-02218974-ML:debug zhongz2$ python task3_step2.py
[Epoch=1, Step=10] loss: 0.653
[Epoch=1, Step=20] loss: 0.474
[Epoch=1, Step=30] loss: 0.245
[Epoch=1, Step=40] loss: 0.080
[Epoch=1, Step=50] loss: 0.017
[Epoch=1, Step=60] loss: 0.006
```












