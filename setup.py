from setuptools import find_packages
from setuptools import setup

setup(
    name = 'epc_fis',
    version = '0.1.0',
    author = 'Iván Bloise Sánchez',
    description= 'Exchange data with FIS database',
    packages=find_packages(),
    entry_points = {
    'console_scripts': [
    'import_cfx=epc_fis.data_load.loader:cfx_main',
    'import_microb=epc_fis.data_load.loader:microb_main',
    'clean_duplicates=epc_fis.data_load.DB_cleaner:main',
    'get_microb_errors=epc_fis.data_load.get_microb_errors:main',
    'check_pcr=epc_fis.data_load.checker:main',
    'calculate_params=epc_fis.data_load.calculate_parameters:main'
    ]
    }
)