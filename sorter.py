import os
from os import path
import shutil

#SETTINGS FOR THE SORTING FUNCTIONS
settings = {
    "main_folder_path": '/mnt/c/Users/User/Downloads',
    "file_extensions": [
        {
            "sort_folder_path": "/mnt/c/Users/User/Downloads/Videos",
            "extensions": ['.mp4', '.mkv', '.m4v', '.avi', '.webm']
        },
        {
            "sort_folder_path": "/mnt/c/Users/User/Downloads/Images",
            "extensions": ['.png', '.jpg', '.jpeg', '.gif']
        },
        {
            "sort_folder_path": "/mnt/c/Users/User/Downloads/Documents",
            "extensions": ['.pdf', '.doc', '.xls']
        },
        {
            "sort_folder_path": "/mnt/c/Users/User/Downloads/Programs",
            "extensions": ['.exe', '.iso']
        },
        {
            "sort_folder_path": "/mnt/c/Users/User/Downloads/Other",
            "extensions": ['.torrent']
        },
        {
            "sort_folder_path": "/mnt/c/Users/User/Downloads/Zip Files",
            "extensions": ['.zip']
        },
    ]
}



# settings = {
#     "main_folder_path": 'C:/Users/Gionne/Downloads',
#     "file_extensions": [
#         {
#             "sort_folder_path": "C:/Users/Gionne/Downloads/Videos",
#             "extensions": ['.mp4', '.mkv', '.m4v', '.avi', '.webm']
#         },
#         {
#             "sort_folder_path": "C:/Users/Gionne/Downloads/Images",
#             "extensions": ['.png', '.jpg', '.jpeg', '.gif']
#         },
#         {
#             "sort_folder_path": "C:/Users/Gionne/Downloads/Documents",
#             "extensions": ['.pdf', '.doc', '.xls']
#         },
#         {
#             "sort_folder_path": "C:/Users/Gionne/Downloads/Programs",
#             "extensions": ['.exe', '.iso']
#         },
#         {
#             "sort_folder_path": "C:/Users/Gionne/Downloads/Other",
#             "extensions": ['.torrent']
#         },
#         {
#             "sort_folder_path": "C:/Users/Gionne/Downloads/Zip Files",
#             "extensions": ['.zip']
#         },
#     ]
# }



#METHOD TO MOVE FILE INTO ITS SORT FOLDER
def moveFile(sort_folder_path, file_path):
 
    destination_path = sort_folder_path + '/' + file_path.rsplit('/', 1)[-1]

    if not path.exists(sort_folder_path):
        os.mkdir(sort_folder_path)   

    shutil.move(file_path, destination_path)



#METHOD TO GET THE DIRECTORY WHERE THE FILE SHOULD BE MOVED
def getSortFolderPath(file_extension):
    for setting in settings['file_extensions']:
        for extension_array in setting['extensions']:
            if file_extension in extension_array:
                return setting["sort_folder_path"]



#METHOD TO GET THE FILE EXTENSION OF A FILE
def getFileExtension(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension


#METHOD TO PRODUCE AN ARRAY OF FOLDERS THAT DOES NOT INCLUDE THE SORT FOLDERS
def filterSortFolders(folder_files):
    excluded_sort_folders_array = []
    for setting in settings['file_extensions']:
        excluded_sort_folders_array.append(setting["sort_folder_path"].rsplit('/', 1)[-1])
    return [x for x in folder_files if x not in excluded_sort_folders_array]



def getFolderItems(main_directory_path):
     for main_directory_files in filterSortFolders(os.listdir(main_directory_path)):
        main_directory_file_path = main_directory_path + '/' + main_directory_files

        #CHECKS IF THE CONTENTS OF THE DIRECTORIES IS A FILE OR FOLDER
        if os.path.isfile(main_directory_file_path):

            #LOOP THROUGH THE FILES AND DETERMINE BY THEIR EXTENSIONS WHERE SHOULD THEY BE MOVED 
            sort_folder_path = getSortFolderPath(getFileExtension(main_directory_files))

            if sort_folder_path:
                moveFile(sort_folder_path, main_directory_file_path)
        else:
            for subdir, sub_directories, sub_directory_files in os.walk(main_directory_file_path):
                for sub_directory_file in sub_directory_files:
                    
                    #LOOP THROUGH THE FILES AND DETERMINE BY THEIR EXTENSIONS WHERE SHOULD THEY BE MOVED 
                    sort_folder_path = getSortFolderPath(getFileExtension(sub_directory_file))

                    if sort_folder_path and path.exists(main_directory_file_path):
                        moveFile(sort_folder_path, main_directory_file_path)


getFolderItems(settings['main_folder_path'])