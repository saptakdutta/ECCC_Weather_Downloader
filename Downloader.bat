@echo off
call activate go_faster

@echo on
python Main.py -wmo_id 71296 -yearUpperRange 2023 -yearLowerRange 2022

@echo off
call conda deactivate
goto :eof