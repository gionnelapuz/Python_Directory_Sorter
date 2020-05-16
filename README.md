# Python Directory Sorter
This is a python script that lets you sort files within a directory based on the file extension. I have created two scripts for sorting and they are **AutoSort.py** and **ManualSort.py**.

* **AutoSort.py**
  * The script will periodically check the folder and sort it without you needing to run the script over and over again, this is basically what I wanted so I just made this script
  
* **ManualSort.py**
  * Lets you just calls the script once if you need to use it.

# How to use
Just replace the paths on the on the **Settings variable** to where the files should go based on their extensions

* **AutoSort.py**

  * Since I am currently using Windows and I want the script to run on startup, I created a **.bat** file to help me with it and will use **pythonw.exe** when calling the script so that the console window wont pop up
  
    * `cd "C:\Users\Name\Python_Directory_Sorter" start pythonw.exe -c "from AutoSort import *; getInput('start')";`
  
  * Start Script: `pythonw.exe -c "from AutoSort import *; getInput('start')";`
  
  * Stop Script: `pythonw.exe -c "from AutoSort import *; getInput('script')";`
  
  
