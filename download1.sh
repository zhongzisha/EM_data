#!/bin/bash


# https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740

SRC_COLLECTION_UUID="47772002-3e5b-4fd3-b97c-18cee38d6df2" # EMBL-EBI Public Data
DST_COLLECTION_UUID="653c6954-44b2-11ee-a070-eb83daae1adf" # local computer

# globus login

globus transfer \
    "${SRC_COLLECTION_UUID}:/pub/databases/IDR/idr0086-miron-micrographs/20200610-ftp/experimentD" \
    "$DST_COLLECTION_UUID:/Users/zhongz2/down/debug/data/EMBL" \
    --recursive --label "EMBL Transfer"




