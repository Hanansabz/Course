import os
import time
from shared.virustotal import scan_file, iterate_files

virustotal_api_key = "cd6325cbf1bd497e7260a5685d37a4772f4784dcad0b0fa47449a224b96fd096"


keepRunning = True
while keepRunning:
    while True:
        NumberOfFiles=len(os.listdir(r"C:\Users\Hanan\Downloads"))
        time.sleep(5)
        OldNumber = NumberOfFiles
        NumberOfFiles = len(os.listdir(r"C:\Users\Hanan\Downloads"))
        if NumberOfFiles != OldNumber:
            print("New file detected! Scanning for viruses...")
            #virus scanning function goes here
            
            directory_path = os.chdir(r"C:\Users\Hanan\Downloads")

            most_recent_file = None
            most_recent_time = 0

            # iterate over the files in the directory using os.scandir
            for entry in os.scandir(directory_path):
                if entry.is_file():
                    mod_time = entry.stat().st_mtime_ns
                    if mod_time > most_recent_time:
                        # update the most recent file and its modification time
                        most_recent_file = entry.name
                        most_recent_time = mod_time
                        
            print(f"Most recent file: {most_recent_file}, downloaded at {most_recent_time}")
            iterate_files(folder_path=most_recent_file, api_key=virustotal_api_key)
