#!/bin/bash


# https://www.ebi.ac.uk/empiar/EMPIAR-11759/

SRC_COLLECTION_UUID="47772002-3e5b-4fd3-b97c-18cee38d6df2"  # EMBL-EBI Public Data
DST_COLLECTION_UUID="653c6954-44b2-11ee-a070-eb83daae1adf"  # local Mac computer

# globus login

globus transfer \
    "${SRC_COLLECTION_UUID}:/empiar/world_availability/11759" \
    "$DST_COLLECTION_UUID:/Users/zhongz2/down/debug/data/EMPIAR-11759" \
    --recursive --label "EMPIAR-11759 Transfer"




