import os
from os import path
import shutil

#SETTINGS FOR THE SORTING FUNCTIONS
settings = {
    "main_folder_path": 'c:/Users/Name/Downloads',

    "exclude_extensions": ['.fdmdownload'],

    "file_extensions": [
        {
            "sort_folder_path": "c:/Users/Name/Downloads/Videos",
            "extensions": ['.mp4', '.mkv', '.m4v', '.avi', '.webm']
        },
        {
            "sort_folder_path": "c:/Users/Name/Downloads/Images",
            "extensions": ['.png', '.jpg', '.jpeg', '.gif']
        },
        {
            "sort_folder_path": "c:/Users/Name/Downloads/Documents",
            "extensions": ['.pdf', '.doc', '.xls']
        },
        {
            "sort_folder_path": "c:/Users/Name/Downloads/Programs",
            "extensions": ['.msi', '.exe', '.iso']
        },
        {
            "sort_folder_path": "c:/Users/Gionne/Downloads/Zip Files",
            "extensions": ['.zip', '.rar', '.7z']
        },
    ]
}


#METHOD TO GET FILENAME AND EXTENSION
def splitFileData(file):
    return list(os.path.splitext(file))


#METHOD TO MOVE FILES/FOLDERS INTO THEIR SORT FOLDER
def moveFile(sort_folder_path, file_path):
    destination_path = sort_folder_path + '/' + file_path.rsplit('/', 1)[-1]

    #CHECKS WHETHER SORT FOLDER EXISTS ALREADY
    if not path.exists(sort_folder_path):
        os.mkdir(sort_folder_path)   

    #CHECKS WHETER FILE/FOLDER ALREADY EXISTS WITHIN THE SORT FOLDER
    if not path.exists(destination_path):
        shutil.move(file_path, destination_path)


#METHOD TO GET THE DIRECTORY WHERE THE FILE SHOULD BE MOVED
def getSortFolderPath(file_extension):
    for setting in settings['file_extensions']:
        for extension_array in setting['extensions']:
            if file_extension in extension_array:
                return setting["sort_folder_path"]


#METHOD TO PRODUCE AN ARRAY OF FOLDERS THAT DOES NOT INCLUDE THE SORT FOLDERS
def filterFolders(folder_files):
    excluded_folders_array = []

    #REMOVES THE SORT FOLDERS FROM SORT ARRAY
    for setting in settings['file_extensions']:
        excluded_folders_array.append(setting["sort_folder_path"].rsplit('/', 1)[-1])
    excluded_folders_array = [x for x in folder_files if x in excluded_folders_array]

    #(OPTIONAL) REMOVES FOLDERS FROM SORT ARRAY THAT CONTAINS EXTENSIONS ADDED ON THE EXCLUDE_EXTENSION SETTINGS
    for excluded_folder_file in folder_files:
        excluded_directory_file_path = settings['main_folder_path'] + '/' + excluded_folder_file
        for subdir, sub_directories, sub_directory_files in os.walk(excluded_directory_file_path):
            for sub_directory_file in sub_directory_files:   
                if splitFileData(sub_directory_file)[1] in settings['exclude_extensions']:
                    excluded_folders_array.append(excluded_folder_file)
                    break
        
    return [x for x in folder_files if x not in excluded_folders_array]


def getFolderFiles():  

    for main_directory_files in filterFolders(os.listdir(settings['main_folder_path'])):
        main_directory_file_path = settings['main_folder_path'] + '/' + main_directory_files

        #CHECKS IF THE CONTENTS OF THE DIRECTORIES IS A FILE OR FOLDER
        if os.path.isfile(main_directory_file_path):

            #LOOP THROUGH THE FILES AND DETERMINE BY THEIR EXTENSIONS WHERE SHOULD THEY BE MOVED 
            sort_folder_path = getSortFolderPath(splitFileData(main_directory_files)[1])

            if sort_folder_path:
                moveFile(sort_folder_path, main_directory_file_path)
        else:
            for subdir, sub_directories, sub_directory_files in os.walk(main_directory_file_path):
                for sub_directory_file in sub_directory_files:
                    
                    #LOOP THROUGH THE FILES AND DETERMINE BY THEIR EXTENSIONS WHERE SHOULD THEY BE MOVED 
                    sort_folder_path = getSortFolderPath(splitFileData(sub_directory_file)[1])

                    if sort_folder_path and path.exists(main_directory_file_path):
                        moveFile(sort_folder_path, main_directory_file_path)


getFolderFiles()