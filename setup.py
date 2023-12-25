# -*- coding: utf-8 -*-
# @Time: 2023/12/24 16:37
# @Author: Administrator
# @File: setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='qfluentPackage',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'PyQt-Fluent-Widgets'
    ],
    # entry_points={
    #     'console_scripts': [
    #         'your_command_name = your_package_name.module_name:main_function'
    #     ]
    # },
    author='fdklgbh',
    author_email='1197804975@qq.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fdklgbh/my_qfluent_utils_package',
)
