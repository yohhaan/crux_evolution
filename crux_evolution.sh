#!/bin/bash

# Variables
years=(2021 2022 2023 2024)
months=(01 02 03 04 05 06 07 08 09 10 11 12)
crux_url=https://github.com/zakird/crux-top-lists/raw/main/data/global/
crux_prefix=crux
crux_dir=./crux/
crux_gz_path=${crux_dir}crux.csv.gz


mkdir -p $crux_dir

#downalod crux
for year in "${years[@]}"
do
    for month in "${months[@]}"
    do
    filename=${crux_dir}${year}${month}.csv
    if [ ! -f $filename ]
    then
        wget -q -O $crux_gz_path ${crux_url}${year}${month}.csv.gz
        gzip -cdk $crux_gz_path > $filename 2>/dev/null
        # on gzip failure delete file (it probably does not exist)
        if [ $? -ne 0 ]; then
            rm $filename
        fi
        rm $crux_gz_path
    fi
    done
done

#generate heatmap
python3 heatmap.py ./crux/ 100000

