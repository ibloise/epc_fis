from cfx_reader import cfx_reader
from microb_reader import microb_reader



cfx_data = cfx_reader(store_files=False)

microb_data = microb_reader()

print(cfx_data)