# Python Directory Sorter
Python script that lets you sort files within a directory based on the file extension. I have created two scripts for sorting and they are **AutoSort.py** and **ManualSort.py**.

* **AutoSort.py**
  * The script will periodically check the folder and sort it without you needing to run the script over and over again, this is basically what I wanted so I just made this script
  
* **ManualSort.py**
  * Lets you just calls the script once if you need to use it.
 
# Requirements
  * [psutil](https://pypi.org/project/psutil/)

# How to use
Just replace the paths on the on the **Settings variable** to where the files should go based on their extensions

* **AutoSort.py**
  
  * **Start Script**: `pythonw.exe -c "from AutoSort import *; getInput('start')";`
  
  * **Stop Script**: `pythonw.exe -c "from AutoSort import *; getInput('stop')";`
  
  
