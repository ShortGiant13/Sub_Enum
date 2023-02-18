#!/usr/bin/env python3

"""
Sub_Enum - A command line tool for enumerating subdomains.
"""

import os
import argparse
import subprocess
from tqdm import tqdm

def main():
    # Prompt the user for the target domain
    target_domain = input("Enter the target domain: ")

    # Prompt the user for the output file path
    output_file = input("Enter the output file path (default: subdomains.txt): ")
    if output_file == "":
        output_file = "subdomains.txt"

    # Run amass to enumerate subdomains
    print("Enumerating subdomains using amass...")
    amass_output_file = "amass_output.txt"
    amass_command = f"amass enum -d {target_domain} -o {amass_output_file}"
    subprocess.run(amass_command, shell=True)

    # Run sublist3r to enumerate subdomains
    print("Enumerating subdomains using sublist3r...")
    sublist3r_output_file = "sublist3r_output.txt"
    sublist3r_command = f"sublist3r -d {target_domain} -o {sublist3r_output_file}"
    subprocess.run(sublist3r_command, shell=True)

    # Merge the output files
    print("Merging output files...")
    with open(output_file, "w") as outfile:
        with open(amass_output_file, "r") as infile:
            for line in tqdm(infile, desc="Processing amass output", unit="lines"):
                outfile.write(line)
        with open(sublist3r_output_file, "r") as infile:
            for line in tqdm(infile, desc="Processing sublist3r output", unit="lines"):
                outfile.write(line)

    # Remove duplicate subdomains from the output file
    print("Removing duplicate subdomains...")
    unique_domains = set()
    with open(output_file, "r") as infile:
        for line in tqdm(infile, desc="Finding unique subdomains", unit="lines"):
            domain = line.strip()
            if domain not in unique_domains:
                unique_domains.add(domain)
    with open(output_file, "w") as outfile:
        for domain in tqdm(unique_domains, desc="Writing output to file", unit="domains"):
            outfile.write(domain + "\n")

    # Clean up the output files
    os.remove(amass_output_file)
    os.remove(sublist3r_output_file)

    print(f"Subdomains enumerated and saved to {output_file}.")

if __name__ == "__main__":
    main()
