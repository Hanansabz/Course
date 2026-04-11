import os
import requests
import time


virustotal_api_scan_url = "https://www.virustotal.com/vtapi/v2/file/scan"
virustotal_api_report_url = "https://www.virustotal.com/vtapi/v2/file/report"
virustotal_api_key = "VT_API_KEY"


def scan_file(file_path):
    response = send_scan_requests(file_path)
    get_report(scan_id=response['scan_id'])

def send_scan_requests(file_path):
    params = {'apikey': virustotal_api_key}


    file_content = open(file_path, 'rb').read()
    file_name = os.path.basename(file_path)
    files = {'file': (file_name, file_content)}

    response = requests.post(virustotal_api_scan_url, files=files, params=params)
    return response.json()



def get_report(scan_id):

    params = {'apikey': virustotal_api_key, 'resource': scan_id}

    response = requests.get(virustotal_api_report_url, params=params)
    if not response:
        raise Exception("Failed to get report from VirusTotal API")
    
    print(response.status_code)


    # if result['verbose_msg'] == "Scan request successfully queued, come back later for the report":
    #     print("Waiting for file to be scanned...")
    #     time.sleep(5)
    #     #get_report(scan_id)
    # else:
    #     print("file scan, positives: ", result["positives"])



def iterate_files(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isdir(full_path):
            iterate_files(full_path)
        else:
            scan_file(full_path)

            





iterate_files(folder_path=r"C:\Users\Hanan\Course\virustest")