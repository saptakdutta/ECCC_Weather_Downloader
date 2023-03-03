#!/bin/bash

cd Documents/Code/Python/ECCC_Weather_Downloader
conda activate base
python Main.py -wmo_id 71296 -yearUpperRange 2024 -yearLowerRange 2022 -outputFormat csv