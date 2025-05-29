#!/bin/bash


# https://www.ebi.ac.uk/empiar/EMPIAR-11759/

SRC_COLLECTION_UUID="47772002-3e5b-4fd3-b97c-18cee38d6df2"  # EMBL-EBI Public Data
DST_COLLECTION_UUID="$(globus endpoint local-id)" # Globus UUID for local computer
DST_SAVE_DIR="$(pwd)/data/EMPIAR-11759"  # local save path

# globus login

globus transfer \
    "${SRC_COLLECTION_UUID}:/empiar/world_availability/11759" \
    "${DST_COLLECTION_UUID}:${DST_SAVE_DIR}" \
    --recursive --label "EMPIAR-11759 Transfer"




