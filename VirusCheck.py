import os
import requests
import time


virustotal_api_scan_url = "https://www.virustotal.com/vtapi/v2/file/scan"
virustotal_api_report_url = "https://www.virustotal.com/vtapi/v2/file/report"
virustotal_api_key = "cd6325cbf1bd497e7260a5685d37a4772f4784dcad0b0fa47449a224b96fd096"


def scan_file(file_path):
    try:
        response = send_scan_requests(file_path)
    except (OSError, requests.RequestException) as e:
        print(f"Error scanning file {file_path}: {e}")
        return

    is_virus = get_report(scan_id=response['scan_id'])
    if is_virus is None:
        print(f"Could not determine status of {file_path} (report unavailable).")
    elif is_virus:
        print(f"File {file_path} is a VIRUS!!!")
    else:
        print(f"File {file_path} is CLEAN.")

def send_scan_requests(file_path):
    params = {'apikey': virustotal_api_key}

    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        file_content = f.read()
    files = {'file': (file_name, file_content)}
    print("Scanning file: ", file_name)
    response = requests.post(virustotal_api_scan_url, files=files, params=params)
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise requests.RequestException(
            f"VirusTotal API scan failed (HTTP {response.status_code}): {response.text}"
        )


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
            raise RuntimeError(
                f"Unexpected VirusTotal response code: {result['response_code']}"
            )
    elif response.status_code == 204:
        print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)
        return get_report(scan_id)
    else:
        raise requests.RequestException(
            f"VirusTotal API report failed (HTTP {response.status_code}): {response.text}"
        )


def iterate_files(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isdir(full_path):
            iterate_files(full_path)
        else:
            scan_file(full_path)

            
#(iterate_files(folder_path=r"C:\Users\Hanan\Course\virustest"))

while True:
    try:
        folder_path = input("Enter the folder path to scan: ")
        iterate_files(folder_path = folder_path)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"Path error: {e}. Please try again.")
    else:
        break
    
input("Press Enter to exit...")