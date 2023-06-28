from setuptools import find_packages
from setuptools import setup

setup(
    name = 'FISDataLoad',
    version = '0.1.0',
    author = 'Iván Bloise Sánchez',
    description= 'Exchange data with FIS database',
    packages=find_packages(),
    entry_points = {
    'console_scripts': [
    'import_cfx=data_load.loader:cfx_main',
    'import_microb=data_load.loader:microb_main',
    'clean_duplicates=data_load.DB_cleaner:main',
    'get_microb_errors=data_load.get_microb_errors:main',
    'check_pcr=data_load.checker:main'
    ]
    }
)