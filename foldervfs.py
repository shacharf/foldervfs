import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import time
import re
import structlog


logger = structlog.get_logger()
ignoreList = [r"swp", r"~", r"bak", r"[0-9]+", r"tmp", r"temp"]


class ReAny:
    """
    Test if a string matches any of the regular expressions
    :param iggnorelist: list of regular expressions
    """

    def __init__(self, ignoreList: list):
        self._ignoreRe = [re.compile(x) for x in ignoreList]

    def __call__(self, string):
        return any(x.search(string) for x in self._ignoreRe)


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, root_folder, vfs_folder, ignoreList_):
        self.root_folder = root_folder
        self.vfs_folder = vfs_folder
        self._is_invalid = ReAny(ignoreList_)

    def on_modified(self, event):
        if not event.is_directory:
            self.copy_to_vfs(event.src_path)

    def copy_to_vfs(self, file_path):
        filename = os.path.basename(file_path)
        if self._is_invalid(filename):
            logger.info(f"Ignoring {filename}")
            return
        version = 1
        vfs_file_path = os.path.join(self.vfs_folder, f"{filename}.v{version}")

        # Increment version number if file already exists
        while os.path.exists(vfs_file_path):
            version += 1
            vfs_file_path = os.path.join(self.vfs_folder, f"{filename}.v{version}")

        try:
            shutil.copy2(file_path, vfs_file_path)
            logger.info(f"Copied {file_path} to {vfs_file_path} as version {version}")
        except:
            logger.info(f"failed to copy {file_path} ==> {vfs_file_path}")


def start_file_monitoring(root_folder, ignoreList):
    vfs_folder = os.path.join(root_folder, ".vfs")
    logger.info(f"vfs folder: {vfs_folder}")
    os.makedirs(vfs_folder, exist_ok=True)

    event_handler = FileChangeHandler(root_folder, vfs_folder, ignoreList)
    observer = Observer()
    observer.schedule(event_handler, root_folder, recursive=False)
    observer.start()
    logger.info(f"Monitoring started on folder: {root_folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


start_file_monitoring(os.path.expanduser(sys.argv[1]), ignoreList)
