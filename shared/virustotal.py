"""Shared VirusTotal API utilities for file scanning and reporting."""

import os
import time
import requests


VIRUSTOTAL_SCAN_URL = "https://www.virustotal.com/vtapi/v2/file/scan"
VIRUSTOTAL_REPORT_URL = "https://www.virustotal.com/vtapi/v2/file/report"


def send_scan_request(file_path, api_key):
    """Upload a file to VirusTotal for scanning."""
    params = {'apikey': api_key}
    file_content = open(file_path, 'rb').read()
    file_name = os.path.basename(file_path)
    files = {'file': (file_name, file_content)}
    print("Scanning file:", file_name)
    response = requests.post(VIRUSTOTAL_SCAN_URL, files=files, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to scan file with VirusTotal API")


def get_report(scan_id, api_key):
    """Retrieve a scan report from VirusTotal, retrying if not ready."""
    params = {'apikey': api_key, 'resource': scan_id}
    response = requests.get(VIRUSTOTAL_REPORT_URL, params=params)

    if response.status_code == 200:
        result = response.json()
        if result['response_code'] == 0:
            print("Report is not ready yet. Waiting for 30 seconds before retrying...")
            time.sleep(30)
            return get_report(scan_id, api_key)
        elif result['response_code'] == 1:
            positives = result['positives']
            total = result['total']
            print(f"Scan results: {positives} positives out of {total} scans.")
            return positives > 0
        elif result['response_code'] == -2:
            print("Report is queued for analysis. Waiting for 30 seconds before retrying...")
            time.sleep(30)
            return get_report(scan_id, api_key)
        else:
            print("Unexpected response code from VirusTotal API:", result['response_code'])
            return None
    elif response.status_code == 204:
        print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)
        return get_report(scan_id, api_key)
    else:
        print("Unexpected error occurred while fetching report from VirusTotal API", response.status_code)
        return None


def scan_file(file_path, api_key):
    """Scan a single file and report whether it is a virus."""
    response = send_scan_request(file_path, api_key)
    is_virus = get_report(scan_id=response['scan_id'], api_key=api_key)
    if is_virus:
        print(f"File {file_path} is a VIRUS!!!")
    else:
        print(f"File {file_path} is CLEAN.")
    return is_virus


def iterate_files(folder_path, api_key):
    """Recursively scan all files in a directory."""
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isdir(full_path):
                iterate_files(full_path, api_key)
            else:
                scan_file(full_path, api_key)
    else:
        scan_file(folder_path, api_key)
