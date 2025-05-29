#!/bin/bash


# https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740

SRC_COLLECTION_UUID="47772002-3e5b-4fd3-b97c-18cee38d6df2" # EMBL-EBI Public Data
DST_COLLECTION_UUID="$(globus endpoint local-id)" # Globus UUID for local computer
DST_SAVE_DIR="$(pwd)/data/EMBL"  # local save path

# globus login

globus transfer \
    "${SRC_COLLECTION_UUID}:/pub/databases/IDR/idr0086-miron-micrographs/20200610-ftp/experimentD" \
    "${DST_COLLECTION_UUID}:${DST_SAVE_DIR}" \
    --recursive --label "EMBL Transfer"




