# Folder-vfs a poor man's Versioning Filesystem
The folder-vfs is a Python-based tool designed to monitor file changes
within a specified folder and automatically back them up with
versioning. This system helps in keeping track of file modifications
and ensures that previous versions are preserved, thereby adding an
extra layer of data protection and recovery.

## Features
* File Monitoring: Continuously watches for changes in the specified folder.
* Automatic Backup: Creates backups of modified files in a dedicated .vfs subdirectory.
* Version Control: Each backed-up file is appended with a version number, allowing easy tracking and retrieval of previous versions.

## Requirements
Python 3

### Installation

Before running the script, ensure Python 3.x is installed on your system. You can then install the required Python module using pip:

```bash
pip install -r requirements.txt
```

## Usage
1. Set Up the Script:

  * Download or clone the repository,
  * In a terminal, navigate to the script's folder,
1. Run the Script:

  * Execute the script using Python with the path to the folder that you wish to monitor. For example:
```bash
python foldervfs.py /path/to/your/directory
```
  * The script will start monitoring the specified directory.

## Viewing Backups:

  * Check the .vfs subdirectory within your monitored directory.
  * Here, you will find the backed-up files with version numbers.

## Configuration & Limitations
* The script is currently set to monitor all file modifications within the specified directory.
* Some files are filtered using the list of regular expressions `ignoreList` in [foldervfs.py](foldervfs.py?plain=1#L12)
* To change the monitoring behavior, edit the script as per your requirements.
* The current implementation does not support real-time backup of newly created files; it only versions modified files.
* Large files and rapid changes might lead to performance issues.
* There is no limit on the number of saved versions or time that they are kept

# Contributing
Contributions are welcome.

# License
This project is open-sourced under the [MIT License](Licence.txt)
