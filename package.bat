@echo off

rd /q /s .\dist .\build .\qfluentPackage.egg-info

python setup.py sdist bdist_wheel

@REM 安装
@REM setlocal enabledelayedexpansion
@REM
@REM for %%f in (.\dist\*.tar.gz) do (
@REM     echo Installing %%f
@REM     pip install "%%~ff"
@REM )
