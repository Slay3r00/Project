#!/usr/bin/env python3

"""STEVE - Secure Toolkit for Examination and Verification of Evidence

This script parses the files in the Chrome data folder, runs various plugins
against the data, and then outputs the results in a spreadsheet.
"""

import argparse
import datetime
import importlib
import logging
import os
import re
import shutil
import sys
import time
import urllib.parse
import ipaddress
import subprocess
# from cloud_modules.aws_config import configure_aws_keys, load_aws_keys // Still working on this
from pyhindsight.analysis import AnalysisSession
from pyhindsight.utils import banner, format_meta_output, format_plugin_output
from OSX_STUFF.file_scraper import find_files, find_segb_files

# Try to import module for timezone support
try:
    import pytz
except ImportError:
    print(f'Could not import module \'pytz\'; all timestamps in XLSX output '
          f'will be in examiner local time ({time.tzname[time.daylight]}).')

print(banner)


def description():
    desc = '''
Overview:
        STEVE (Systematic Tool for Evidence Verification and Examination) is a powerful, all-in-one digital forensics
        and incident response (DFIR) tool designed to streamline the investigation process for modern web
        browsers and cloud service providers. STEVE specializes in analyzing browsing data from Chrome,
        Chromium, and Safari, while also providing robust capabilities for extracting secrets from major
        cloud service providers including GCP, AWS, Azure, and many others. 
            '''
    print(desc)


def print_menu():
    print("""
    Select from the menu:
    
    1) Browser Forensics (Chrome, Chromium, Safari)
    2) Cache Extraction
    3) Extract Secrets (GCP, AWS, Azure, and more)
    4) Configure AWS Keys
    5) OSX File Scraper (Juicy info)
    99) Exit
    """)


def print_browser_menu():
    print("""
    Select the browser type:
    
    1) Chrome
    2) Safari
    3) Firefox
    99) Back to Main Menu
    """)


def run_browser_forensics():
    print("Running forensics for Chrome...")
    input_path = input("Enter the input path to the browser profile directory: ").strip()
    output_name = input("Enter the output file name (without extension): ").strip()
    file_type = input("Enter the file type for output (xlsx, sqlite, jsonl): ").strip().lower()
    cmd = f"python main.py -i {input_path} -o {output_name} -f {file_type}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")


def run_osx_file_scraper():
    starting_directory = input("Enter the starting directory for the search: ").strip()
    file_type = input("Enter the type of files to search for (db, plist, ips, segb): ").strip().lower()
    output_file = input("Enter the path to the output file (optional): ").strip()

    if not os.path.isdir(starting_directory):
        print("Invalid directory path.")
        return

    if file_type == 'segb':
        found_files = find_segb_files(starting_directory)
    else:
        found_files = find_files(starting_directory, file_type)

    if output_file:
        with open(output_file, "w") as f:
            for file_path in found_files:
                f.write(file_path + "\n")
        print(f"Output written to {output_file}")
    else:
        for file_path in found_files:
            print(file_path)


def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            print_browser_menu()
            browser_choice = input("Select a browser: ").strip().lower()
            if browser_choice == "chrome":
                run_browser_forensics()
            elif browser_choice == "1":
                run_browser_forensics()
            else:
                print("Currently, only Chrome is supported for Browser Forensics.")
        elif choice == '2':
            # Placeholder for Cache Collector functionality
            print("Cache Collector functionality is not yet implemented.")
        elif choice == '3':
            # Placeholder for Extract Cloud Secrets functionality
            print("Extract Cloud Secrets functionality is not yet implemented.")
        elif choice == "4":
            # Configure AWS keys
           # configure_aws_keys()
           print("Not yet configured")
        elif choice == '5':
            run_osx_file_scraper()
        elif choice == '99':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
