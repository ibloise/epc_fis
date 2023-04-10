import os

def return_files(folder, full_path = True):
    """
    return list of files paths. If full_path, return absolute paths.
    """
    return [os.path.abspath(os.path.join(folder, file)) if full_path else file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]