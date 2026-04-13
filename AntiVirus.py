import os
import requests
import time

virustotal_api_scan_url = "https://www.virustotal.com/vtapi/v2/file/scan"
virustotal_api_report_url = "https://www.virustotal.com/vtapi/v2/file/report"
virustotal_api_key = "cd6325cbf1bd497e7260a5685d37a4772f4784dcad0b0fa47449a224b96fd096"


def scan_file(file_path):
    response = send_scan_requests(file_path)
    # if not response:
    #     return  # skip this file completely
    is_virus = get_report(scan_id=response['scan_id'])
    if is_virus:
        print(f"File {file_path} is a VIRUS!!!")
    else:
        print(f"File {file_path} is CLEAN.")

def send_scan_requests(file_path):
    params = {'apikey': virustotal_api_key}

    file_content = open(file_path, 'rb').read()
    file_name = os.path.basename(file_path)
    files = {'file': (file_name, file_content)}
    print("Scanning file: ", file_name)
    response = requests.post(virustotal_api_scan_url, files=files, params=params)
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise Exception("Failed to scan file with VirusTotal API")


def get_report(scan_id):
    params = {'apikey': virustotal_api_key, 'resource': scan_id}
    response = requests.get(virustotal_api_report_url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if result['response_code'] == 0:
            print("Report is not ready yet. Waiting for 30 seconds before retrying...")
            time.sleep(30)
            return get_report(scan_id)
        elif result['response_code'] == 1:
            positives = result['positives']
            total = result['total']
            print(f"Scan results: {positives} positives out of {total} scans.")
            return positives > 0
        elif result['response_code'] == -2:
            print("Report is queued for analysis. Waiting for 30 seconds before retrying...")
            time.sleep(30)
            return get_report(scan_id)
        else:
            print("Unexpected response code from VirusTotal API:", result['response_code'])
            return None
    elif response.status_code == 204:
        print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)
        return get_report(scan_id)
    else:
        print("Unexpected error occurred while fetching report from VirusTotal API", response.status_code)


def iterate_files(folder_path):
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isdir(full_path):
                iterate_files(full_path)
            else:
                scan_file(full_path)
    else:
        scan_file(folder_path)


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
                        
            print(f"Most recent file: {most_recent_file}")
            iterate_files(folder_path = most_recent_file)
        