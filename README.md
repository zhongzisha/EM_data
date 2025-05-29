

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












