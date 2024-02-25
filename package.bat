@echo off

rd /q /s .\dist .\build .\qfluentPackage.egg-info

python setup.py sdist bdist_wheel

@REM 安装
setlocal enabledelayedexpansion

for %%f in (.\dist\*.tar.gz) do (
    echo Installing %%f
    pip install "%%~ff"
)
