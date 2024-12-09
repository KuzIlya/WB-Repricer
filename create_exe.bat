@echo off

echo Installing project libs...
pip install -r requirements.txt

echo Installing pysimplegui-exemaker...
pip install pysimplegui-exemaker

echo Running pysimplegui-exemaker...
python -m pysimplegui-exemaker.pysimplegui-exemaker

echo Moving and renaming main.exe to repricer.exe...
set script_dir=%~dp0
set target_file=%script_dir%\main.exe
set dest_file=%script_dir%repricer.exe

if exist "%target_file%" (
    move "%target_file%" "%dest_file%"
    echo File moved and renamed successfully.
) else (
    echo Error: main.exe not found in app directory.
)

pause
