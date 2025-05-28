#!/bin/bash


# https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2

SRC_COLLECTION_UUID="4422e452-f97e-4cdd-ad88-7cecf14aa258"  # Janelia COSEM Datasets - OpenOrganelle
DST_COLLECTION_UUID="653c6954-44b2-11ee-a070-eb83daae1adf"  # local computer

# globus login

globus transfer \
    "${SRC_COLLECTION_UUID}:/jrc_mus-nacc-2/" \
    "$DST_COLLECTION_UUID:/Users/zhongz2/down/debug/data/jrc_mus-nacc-2/" \
    --recursive --label "Janelia COSEM Datasets Transfer"




