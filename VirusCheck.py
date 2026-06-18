import os
from shared.virustotal import scan_file, iterate_files

virustotal_api_key = "cd6325cbf1bd497e7260a5685d37a4772f4784dcad0b0fa47449a224b96fd096"


#(iterate_files(folder_path=r"C:\Users\Hanan\Course\virustest"))

while True:
    try:
        folder_path = input("Enter the folder path to scan: ")
        iterate_files(folder_path=folder_path, api_key=virustotal_api_key)
    except Exception as e:
        print("Incorrect path, please try again.")
    else:
        break
    
input("Press Enter to exit...")
