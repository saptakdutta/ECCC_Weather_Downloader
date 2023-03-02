@echo off
call activate go_faster

@echo on
python Main.py -wmo_id 71296 -yearUpperRange 2024 -yearLowerRange 2022 -outputFormat csv

@echo off
call conda deactivate
goto :eof