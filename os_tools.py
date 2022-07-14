import os

#this function will return all the directory paths in a directory
def get_sub_paths(input_path):

    ''' Take in a path, return a list of sub folder paths'''

    ppaths = []

    for path, sub_dirs, files in os.walk(input_path):

        ppaths.append(path)

    return ppaths

#function to iterate through the list and find the ones that end with 'nifti'

def find_nifti(directory_list:list) -> list:

    '''
    This function splits a list of directory paths at the \\ character
    Then it splits the folder name, and looks for nifti at the end
    If it finds that, it adds the file path to a list
    '''

    nif_list = []

    for path in directory_list:


        #make a list and split out the path
        dirs_list = path.split('\\')

        #split out the last entry in the path
        end_list = dirs_list[-1].split('_')

        #see if the third entry is nifti and append path if so
        if end_list[-1] == 'nifti':

           nif_list.append(path)

    return nif_list