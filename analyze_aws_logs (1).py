#1
# ## process all the files from processed_outputs (Loops) (create one single log file combined  all processed_outputs)
# import os
# import re
# from collections import defaultdict
#
# # Define paths
# INPUT_FOLDER = "./processed_outputs"  # Folder containing AWS IoT logs
# OUTPUT_ANALYSIS_FILE = "./analysis_results.log"  # File for extracted log lines
# SUMMARY_REPORT_FILE = "./summary_report.log"  # File for issue summary
#
# # Define regex patterns to extract relevant log entries
# PATTERNS = {
#     "status": r"(AWSIOT_STATUS_[A-Z_]+)",
#     "network_failed": r"no connectivity to cloud server",
#     "network_success": r"connectivity to cloud server is good!",
#     "dns_timeout": r"no connectivity to cloud server due to DNS timeout",
#     "dns_getaddrinfo": r"getaddrinfo failed with error: -2\(Name or service not known\)"
# }
#
# # Issue tracking
# issue_summary = defaultdict(int)
# total_logs = 0
#
# # Ensure input folder exists
# if not os.path.exists(INPUT_FOLDER):
#     print(f"Error: Folder '{INPUT_FOLDER}' does not exist.")
#     exit(1)
#
# # Open analysis file for writing extracted log lines
# with open(OUTPUT_ANALYSIS_FILE, "w", encoding="utf-8") as analysis_output:
#
#     # Process each log file in the folder
#     for filename in os.listdir(INPUT_FOLDER):
#         file_path = os.path.join(INPUT_FOLDER, filename)
#
#         # Skip directories, process only files
#         if not os.path.isfile(file_path):
#             continue
#
#         total_logs += 1
#         print(f"Processing: {filename}")
#
#         # Tracking per-file issue status
#         last_status = None
#         last_issue = None
#         status_sequence = []
#         network_success_seen = False
#
#         # Read and analyze the log file
#         with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
#             for line in infile:
#                 # Extract AWS IoT statuses
#                 status_match = re.search(PATTERNS["status"], line)
#                 if status_match:
#                     last_status = status_match.group(0)
#                     status_sequence.append(last_status)
#
#                 # Check for network connectivity and DNS issues
#                 if re.search(PATTERNS["network_failed"], line):
#                     last_issue = "Network Failure"
#                 elif re.search(PATTERNS["network_success"], line):
#                     network_success_seen = True
#                 elif re.search(PATTERNS["dns_timeout"], line):
#                     last_issue = "DNS Timeout"
#                 elif re.search(PATTERNS["dns_getaddrinfo"], line):
#                     last_issue = "DNS Resolution Error"
#
#                 # Save extracted log lines
#                 if any(re.search(pattern, line, re.IGNORECASE) for pattern in PATTERNS.values()):
#                     analysis_output.write(f"[{filename}] {line}")
#
#         # Determine the root cause based on the last timestamp event
#         if last_status == "AWSIOT_STATUS_CONNECTING" and last_issue:
#             issue_summary[last_issue] += 1
#         elif last_status == "AWSIOT_STATUS_CONNECTING" and not last_issue:
#             issue_summary["Unknown Connection Issue"] += 1
#         elif network_success_seen:
#             issue_summary["Successful Connections"] += 1
#
# # Write summary report
# with open(SUMMARY_REPORT_FILE, "w", encoding="utf-8") as summary_output:
#     summary_output.write("AWS IoT Log Analysis Summary\n")
#     summary_output.write("=" * 40 + "\n")
#     summary_output.write(f"Total log files processed: {total_logs}\n")
#     for category, count in issue_summary.items():
#         summary_output.write(f"{category}: {count} logs affected\n")
#
# print("\nAnalysis complete. Results saved:")
# print(f"- Extracted log details: {OUTPUT_ANALYSIS_FILE}")
# print(f"- Summary report: {SUMMARY_REPORT_FILE}")
# print(f"- Analysis file: {OUTPUT_ANALYSIS_FILE}")









#2
#process all the files from processed_outputs (Loops) (create seperate log file for  each processed_outputs)
import os
import re
from collections import defaultdict

# Define paths
INPUT_FOLDER = "/Users/ruthik.nataraja/Desktop/My Real log/logX-predone/processed_outputs-IOTOFFLINE"  # Folder containing AWS IoT logs
OUTPUT_FOLDER = "./log_files"  # Folder to store individual log files
SUMMARY_REPORT_FILE = "./summary_report.log"  # File for issue summary

# Define regex patterns to extract relevant log entries
PATTERNS = {
    "status": r"(AWSIOT_STATUS_[A-Z_]+)",
    "network_failed": r"no connectivity to cloud server",
    "network_success": r"connectivity to cloud server is good!",
    "dns_timeout": r"no connectivity to cloud server due to DNS timeout",
    "dns_getaddrinfo": r"getaddrinfo failed with error: -2\(Name or service not known\)"
}

# Issue tracking
issue_summary = defaultdict(int)
total_logs = 0

# Ensure input folder exists
if not os.path.exists(INPUT_FOLDER):
    print(f"Error: Folder '{INPUT_FOLDER}' does not exist.")
    exit(1)

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Open summary file for writing the issue summary
with open(SUMMARY_REPORT_FILE, "w", encoding="utf-8") as summary_output:
    summary_output.write("AWS IoT Log Analysis Summary\n")
    summary_output.write("=" * 40 + "\n")

    # Process each log file in the folder
    for filename in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, filename)

        # Skip directories, process only files
        if not os.path.isfile(file_path):
            continue

        total_logs += 1
        print(f"Processing: {filename}")

        # Tracking per-file issue status
        last_status = None
        last_issue = None
        status_sequence = []
        network_success_seen = False

        # Open a new output file for each log file processed
        output_file_path = os.path.join(OUTPUT_FOLDER, f"{filename}_analysis.log")
        with open(output_file_path, "w", encoding="utf-8") as analysis_output:

            # Read and analyze the log file
            with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                for line in infile:
                    # Extract AWS IoT statuses
                    status_match = re.search(PATTERNS["status"], line)
                    if status_match:
                        last_status = status_match.group(0)
                        status_sequence.append(last_status)

                    # Check for network connectivity and DNS issues
                    if re.search(PATTERNS["network_failed"], line):
                        last_issue = "Network Failure"
                    elif re.search(PATTERNS["network_success"], line):
                        network_success_seen = True
                    elif re.search(PATTERNS["dns_timeout"], line):
                        last_issue = "DNS Timeout"
                    elif re.search(PATTERNS["dns_getaddrinfo"], line):
                        last_issue = "DNS Resolution Error"

                    # Save extracted log lines if they match any patterns
                    if any(re.search(pattern, line, re.IGNORECASE) for pattern in PATTERNS.values()):
                        analysis_output.write(f"[{filename}] {line}")

            # Determine the root cause based on the last timestamp event
            if last_status == "AWSIOT_STATUS_CONNECTING" and last_issue:
                issue_summary[last_issue] += 1
            elif last_status == "AWSIOT_STATUS_CONNECTING" and not last_issue:
                issue_summary["Unknown Connection Issue"] += 1
            elif network_success_seen:
                issue_summary["Successful Connections"] += 1

    # Write summary report
    summary_output.write(f"Total log files processed: {total_logs}\n")
    for category, count in issue_summary.items():
        summary_output.write(f"{category}: {count} logs affected\n")

print("\nAnalysis complete. Results saved:")
print(f"- Individual log files are stored in the '{OUTPUT_FOLDER}' folder.")
print(f"- Summary report: {SUMMARY_REPORT_FILE}")



















