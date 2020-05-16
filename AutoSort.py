import os
from os import path
import shutil

import psutil
import time
from datetime import datetime

#VARIABLES NEEDED FOR AUTO SORTING
start_watch = True
pid_txt_loc = 'pid.txt'
log_txt_loc = 'status.log'

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
            "sort_folder_path": "c:/Users/Name/Downloads/Zip Files",
            "extensions": ['.zip', '.rar', '.7z']
        },
    ]
}


#METHOD THAT WRITES TO TEXT FILES
def writeToTextFile(file_loc, type, text):
    if not path.exists(file_loc):
        txt_file = open(file_loc, type)
        txt_file.write(text)
        txt_file.close()  

    txt_file = open(file_loc, type)
    txt_file.write(text)
    txt_file.close()
    

#METHOD THAT WRITES THE UNIQUE PROCESS ID TO THE TEXT FILE
def writePID():
    p_id = os.getpid()
    p_name = psutil.Process(p_id).name()
    writeToTextFile(pid_txt_loc, 'a', str(p_id) + ':' + p_name)


#METHOD THAT TERMINATES THE PROCESS ID
def terminatePID():
    if open("pid.txt", "r").read():
        txt_file = open("pid.txt", "r")
        process_detail = txt_file.read().rsplit(':', 1)
        p_id = int(process_detail[0])
        p_name = process_detail[1]
        p = psutil.Process(p_id)
        p.terminate()

        writeToTextFile(pid_txt_loc, 'w', '')
        writeToTextFile(log_txt_loc, 'w', '')
        return


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


#METHOD THAT STARTS THE SORT
def startAutoSort():
    writePID()
    while start_watch:
        #(OPTIONAL) LOG EACH TIME THE SORT RUNS
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        writeToTextFile(log_txt_loc, 'a', 'Sorting Ran' + ' : '  + date_time + '\n')
        
        getFolderFiles()
        time.sleep(60)


#METHOD THAT CHECKS IF THE AUTO SORT IS ALREADY RUNNING
def checkProcessRunning():
    if not path.exists(pid_txt_loc):
        writeToTextFile(pid_txt_loc, 'w', '')
        

    if open(pid_txt_loc, "r").read():
        txt_file = open(pid_txt_loc, "r")
        process_detail = txt_file.read().rsplit(':', 1)
        p_id = int(process_detail[0])
        p_name = process_detail[1]

        for proc in psutil.process_iter():
            #IF PROCESS IS ALREADY RUNNING LOG IT
            if proc.pid == p_id and proc.name() == p_name:
                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                writeToTextFile(log_txt_loc, 'a', 'Process is Already Running' + ' : '  + date_time + '\n')
                return  

        #IF PID IS FOUND IN TEXT FILE BUT ISN'T RUNNING THEN RESTART THE AUTO SORT WITH A NEW PID
        writeToTextFile(pid_txt_loc, 'w', '')
        writeToTextFile(log_txt_loc, 'w', '')
        startAutoSort()
        return
    else:
        #IF NO PID IS FOUND IN TEXT FILE THEN START AUTO SORT
        startAutoSort()


#METHOD INPUT FROM TERMINAL TO DETERMINE WHAT TO DO
def getInput(todo):
    if todo == 'start':
        checkProcessRunning()

    elif todo == 'stop':
        terminatePID()