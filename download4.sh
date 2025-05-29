#!/bin/bash


# https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2

SRC_COLLECTION_UUID="4422e452-f97e-4cdd-ad88-7cecf14aa258"  # Janelia COSEM Datasets - OpenOrganelle
DST_COLLECTION_UUID="$(globus endpoint local-id)" # Globus UUID for local computer
DST_SAVE_DIR="$(pwd)/data/jrc_mus-nacc-2/"  # local save path

# globus login

globus transfer \
    "${SRC_COLLECTION_UUID}:/jrc_mus-nacc-2/" \
    "${DST_COLLECTION_UUID}:${DST_SAVE_DIR}" \
    --recursive --label "Janelia COSEM Datasets Transfer"




