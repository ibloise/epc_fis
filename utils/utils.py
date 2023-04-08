import os

def return_files(folder, full_path = True, folder_sep = "/"):
    """
    return list of files paths. If full_path, return absolute paths.
    """
    return [os.path.abspath(folder_sep.join([folder, file])) if full_path else file for file in os.listdir(folder)]