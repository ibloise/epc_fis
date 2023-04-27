import os

def return_files(folder, full_path = True):
    """
    return list of files paths. If full_path, return absolute paths.
    """
    return [os.path.abspath(os.path.join(folder, file)) if full_path else file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]

def store_file(file, store_folder):
    """
    Function to store files. Create folder if necessary.
    """
    import shutil
    import filecmp
    import os
    if not os.path.exists(store_folder):
        os.mkdir(store_folder)
    filename = os.path.basename(file)
    shutil.copyfile(file, os.path.join(store_folder, filename))
    if filecmp.cmp(file, os.path.join(store_folder, filename)): #Compare copy file with original file before delete original file.
        #¿¿Y si lo cambiamos a shutil.move????
        os.remove(file)
    else:
        print(f"Error in {file} management")