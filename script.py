#1
#process all  files from SampleOFFlinelogs (loop)
import subprocess
import os
import re
import shutil
from natsort import natsorted  # Natural sorting for correct numeric order

# Define the folder containing input files
input_folder = "logs" #Your input folder
script_path = "devicelog"
output_folder = "output" #Your output folder

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Dictionary to store extracted IoT current values
iotclient_results = {}

# Ensure the input folder exists
if not os.path.exists(input_folder):
    print(f"Error: Folder '{input_folder}' does not exist.")
    exit(1)

# Match files like syslog.log.33
input_files = [
    f for f in os.listdir(input_folder)
    if os.path.isfile(os.path.join(input_folder, f)) and re.match(r"^syslog\.log\.\d+$", f)
]

for filename in input_files:
    file_path = os.path.join(input_folder, filename)
    print(f"\nProcessing: {file_path}")

    # Run the script using the current file as input
    subprocess.run([script_path, file_path], check=True)

    # Detect multiple output files (assuming they all start with "z" or are named "syslog.log")
    output_files = [
        f for f in os.listdir(os.getcwd())
        if f.startswith("z") or f.startswith("syslog.log")
    ]

    # Sort output files numerically
    sorted_output_files = natsorted(output_files)

    # Define the renamed output file path
    renamed_output_file = os.path.join(output_folder, f"{filename}_output.log")

    # Define the filtered output file path (only "iotclient" lines)
    filtered_output_file = os.path.join(output_folder, f"{filename}_iotclient.log")

    # Combine multiple output files into one
    with open(renamed_output_file, "wb") as outfile:
        for out_file in sorted_output_files:
            with open(out_file, "rb") as infile:
                print(f"Writing {out_file}")
                shutil.copyfileobj(infile, outfile)
            os.remove(out_file)

    print(f"Aggregated {len(sorted_output_files)} files into '{renamed_output_file}'")

    # Rename 'zcurrent' if exists
    original_output_file = os.path.join(os.getcwd(), "zcurrent")
    if os.path.exists(original_output_file):
        os.rename(original_output_file, renamed_output_file)
        print(f"Renamed 'zcurrent' to '{renamed_output_file}'")
    else:
        print(f"Warning: 'zcurrent' file not found for {filename}")

    # Extract lines with "iotclient"
    iotclient_values = []
    try:
        with open(renamed_output_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "iotclient" in line.lower():
                    iotclient_values.append(line.strip())
    except UnicodeDecodeError:
        print(f"Warning: Could not decode '{renamed_output_file}', skipping parsing.")

    # Store results
    iotclient_results[filename] = iotclient_values

print("\nExtraction complete. Results saved:")






#
# #2
# #process onefiles from SampleOFFlinelogs (No loop)
# import subprocess
# import os
# import re
# import shutil
# from natsort import natsorted
#
# # Define paths for a single specific file
# input_file = "/Users/ruthik.nataraja/Desktop/My Real log/logX-predone/KVS - Uploading issuelog/syslog.log.1"
# script_path = "/Users/ruthik.nataraja/Desktop/My Real log/logX-predone/devicelog"
# output_folder = "/Users/ruthik.nataraja/Desktop/My Real log/logX-predone/processed_outputs"
#
# # Ensure the output folder exists
# os.makedirs(output_folder, exist_ok=True)
#
# # Check if the specific input file exists
# if not os.path.exists(input_file):
#     print(f"Error: File '{input_file}' does not exist.")
#     exit(1)
#
# # Get just the filename for processing
# filename = os.path.basename(input_file)
# print(f"Processing single file: {input_file}")
#
# # Run the script using the specific file as input
# subprocess.run([script_path, input_file], check=True)
#
# # Detect output files (assuming they all start with "z" or are named "syslog.log")
# output_files = [
#     f for f in os.listdir(os.getcwd())
#     if f.startswith("z") or f.startswith("syslog.log")
# ]
#
# # Sort output files numerically
# sorted_output_files = natsorted(output_files)
#
# # Define the renamed output file path
# renamed_output_file = os.path.join(output_folder, f"{filename}_output.log")
#
# # Define the filtered output file path (only "iotclient" lines)
# filtered_output_file = os.path.join(output_folder, f"{filename}_iotclient.log")
#
# # Combine multiple output files into one (if any exist)
# if sorted_output_files:
#     with open(renamed_output_file, "wb") as outfile:
#         first_file = sorted_output_files[0]
#         with open(first_file, "rb") as infile:
#             print(f"Writing {first_file}")
#             shutil.copyfileobj(infile, outfile)
#         os.remove(first_file)
#
#         # If there are additional files, append them
#         if len(sorted_output_files) > 1:
#             second_file = sorted_output_files[1]
#             with open(second_file, "rb") as infile:
#                 print(f"Appending {second_file}")
#                 shutil.copyfileobj(infile, outfile)
#             os.remove(second_file)
#
#         # If there's a third file, append it too
#         if len(sorted_output_files) > 2:
#             third_file = sorted_output_files[2]
#             with open(third_file, "rb") as infile:
#                 print(f"Appending {third_file}")
#                 shutil.copyfileobj(infile, outfile)
#             os.remove(third_file)
#
#     print(f"Combined {len(sorted_output_files)} files into '{renamed_output_file}'")
#
# # Handle 'zcurrent' file if it exists
# original_output_file = os.path.join(os.getcwd(), "zcurrent")
# if os.path.exists(original_output_file):
#     os.rename(original_output_file, renamed_output_file)
#     print(f"Renamed 'zcurrent' to '{renamed_output_file}'")
# else:
#     print(f"Warning: 'zcurrent' file not found for {filename}")
#
# # Extract lines with "iotclient" without using a loop
# iotclient_values = []
# try:
#     with open(renamed_output_file, "r", encoding="utf-8", errors="ignore") as f:
#         content = f.read()
#         # Split content into lines and filter for iotclient
#         lines = content.split('\n')
#         # Use list comprehension instead of loop
#         iotclient_values = [line.strip() for line in lines if "iotclient" in line.lower() and line.strip()]
# except UnicodeDecodeError:
#     print(f"Warning: Could not decode '{renamed_output_file}', skipping parsing.")
# except FileNotFoundError:
#     print(f"Warning: Output file '{renamed_output_file}' not found.")
#
# # Save iotclient lines to filtered file
# if iotclient_values:
#     with open(filtered_output_file, "w", encoding="utf-8") as f:
#         # Write all iotclient lines at once
#         f.write('\n'.join(iotclient_values))
#     print(f"Saved {len(iotclient_values)} iotclient lines to '{filtered_output_file}'")
# else:
#     print("No iotclient lines found in the processed file.")
#
# print(f"\nProcessing complete for: {filename}")
# print(f"Output file: {renamed_output_file}")
# print(f"Filtered file: {filtered_output_file}")
# print(f"Total iotclient lines found: {len(iotclient_values)}")
#
#
#










