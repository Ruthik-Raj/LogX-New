##Before code
# import ollama
# import re
#
# # Step 1: Read the log file
# file_path = "/Users/ruthik.nataraja/Desktop/logX-predone/log_files"
# with open(file_path, "r", encoding="utf-8") as file:
#     file_content = file.read()
#
# # Step 2: Prompt to generate one Q&A
# custom_prompt = (
#     "From the following log, output exactly one question and one answer in this format:\n"
#     "Question: <one-line question>\n"
#     "Answer: <one-line answer>\n"
#     "Do not add any explanations, preambles, or extra text. Just the question and answer.\n\n"
#     "Log:\n"
# )
# full_prompt = f"{custom_prompt}{file_content}"
#
# response = ollama.chat(model='deepseek-r1', messages=[{"role": "user", "content": full_prompt}])
# response_text = response["message"]["content"]
#
# # Step 3: Prompt to generate a 10-word question from the Q&A
# custom_prompt2 = (
#     "Generate a question from the following text using exactly 10 words. "
#     "Only return the 10-word question. No explanations, thoughts,  No explaination, No recomendations or formatting:\n\n"
#     "Text:\n"
# )
# full_prompt2 = f"{custom_prompt2}{response_text}"
#
# response2 = ollama.chat(model='deepseek-r1', messages=[{"role": "user", "content": full_prompt2}])
# response_text2 = response2["message"]["content"]
#
# # Step 4: Remove <think> block and extract the actual question
# cleaned_output = re.sub(r"<think>.*?</think>", "", response_text2, flags=re.DOTALL).strip()
#
# # Extract the first valid question line ending in ?
# match = re.search(r"([A-Z][^.?!]*\?)", cleaned_output)
# question_only = match.group(1).strip() if match else cleaned_output.strip()
#
# # Step 5: Print the final result
# print("Question:\n", question_only)



#root cause, firmware, timestamp ( No loop)
import ollama
import re
import os
from datetime import datetime

# === File setup ===
file_path = "Your file location"
# Get the first log file or specify a specific file
log_files = [
    os.path.join(file_path, fname)
    for fname in os.listdir(file_path)
    if os.path.isfile(os.path.join(file_path, fname))
]

# Process a single log file (first one in the list)
if log_files:
    log_file = log_files[0]  # Take the first file

    with open(log_file, "r", encoding="utf-8", errors="replace") as file:
        file_content = file.read()

    # === Extract relevant NETWORK lines for LLM ===
    network_lines = [
        line for line in file_content.split('\n')
        if "NETWORK[INFO][netservice.c:net_service_thread" in line
    ]
    prompt_detail = "From the following NETWORK thread log lines, explain in detail what the log is about:\n"
    network_log_text = '\n'.join(network_lines)
    full_prompt = f"{prompt_detail}{network_log_text}"

    response = ollama.chat(model='llama3.2:latest', messages=[{"role": "user", "content": full_prompt}])
    response_text = response["message"]["content"]

    # === 15-word summary prompt ===
    prompt_summary = (
        "You are an expert in understanding logs and tell what is the log about so take these lines and Explain briefly the root cause of the issue in 20 words.\n"
        "QUESTION: <your 20-word summary>"
    )
    full_prompt2 = f"{prompt_summary}\n{response_text}"
    response2 = ollama.chat(model='llama3.2:latest', messages=[{"role": "user", "content": full_prompt2}])
    summary_output = response2["message"]["content"]

    question_match = re.search(r'QUESTION:\s*(.+)', summary_output)
    question_only = question_match.group(1).strip() if question_match else summary_output.strip()

    # === Firmware Extraction ===
    firmware_match = re.search(r'Firmware version from file\s*:\s*\[([^\]]+)\]', file_content)
    firmware_version = firmware_match.group(1).strip() if firmware_match else "Firmware version not available"

    # === USERID Extraction ===
    filename = os.path.basename(log_file)
    userid_match = re.search(r"(?:log_)?([A-F0-9]{6,}(_\d+)?|\d+)", filename, re.IGNORECASE)
    userid = userid_match.group(1) if userid_match else "unknown"

    # === Timestamp from first NETWORK[INFO][netservice.c:net_service_thread] line ===
    timestamp_pattern = r"([A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}\.\d{3})"
    log_time = None
    error_message = None

    for line in file_content.split('\n'):
        if "NETWORK[INFO][netservice.c:net_service_thread" in line:
            match = re.search(timestamp_pattern, line)
            if match:
                timestamp_str = match.group(1)
                try:
                    timestamp_str_with_year = f"{datetime.now().year} {timestamp_str}"
                    log_time = datetime.strptime(timestamp_str_with_year, "%Y %b %d %H:%M:%S.%f")
                except ValueError:
                    log_time = None
            error_message = line.strip()  # Save the entire line as the error message
            break  # Only take the first occurrence

    # === MAC Address Extraction ===
    mac_pattern = r'(?:[0-9A-Fa-f]{12})'
    mac_matches = re.findall(mac_pattern, file_content)
    mac_address = mac_matches[0] if mac_matches else "MAC address not found"

    file_type_value = "IOT logs"

    # === Output Results ===
    print(f"Processed file: {filename}")
    print("USERID:", userid)
    print("File Type:", file_type_value)
    print("Question:\n", question_only)
    print("Time:\n", f"{log_time} : {error_message}" if log_time and error_message else "No NETWORK timestamp found.")
    print("MAC Address:\n", mac_address)
    print("Firmware Version:\n", firmware_version)
    print("-" * 50)

    # === Return extracted data as dictionary ===
    extracted_data = {
        'filename': filename,
        'userid': userid,
        'file_type': file_type_value,
        'question': question_only,
        'log_time': log_time,
        'error_message': error_message,
        'mac_address': mac_address,
        'firmware_version': firmware_version
    }

else:
    print("No log files found in the specified directory.")



##root cause, firmware, timestamp (looped )
# import ollama
# import re
# import os
# from datetime import datetime
#
# # === File setup ===
# file_path = "/content/drive/MyDrive/processed_outputs-IOTOFFLINE"
# log_files = [
#     os.path.join(file_path, fname)
#     for fname in os.listdir(file_path)
#     if os.path.isfile(os.path.join(file_path, fname))
# ]
#
# # === Process Each Log File ===
# for log_file in log_files:
#     with open(log_file, "r", encoding="utf-8", errors="replace") as file:
#         file_content = file.read()
#
#     # === Extract relevant NETWORK lines for LLM ===
#     network_lines = [
#         line for line in file_content.split('\n')
#         if "NETWORK[INFO][netservice.c:net_service_thread" in line
#     ]
#     prompt_detail = "From the following NETWORK thread log lines, explain in detail what the log is about:\n"
#     network_log_text = '\n'.join(network_lines)
#     full_prompt = f"{prompt_detail}{network_log_text}"
#
#     response = ollama.chat(model='llama3.2:latest', messages=[{"role": "user", "content": full_prompt}])
#     response_text = response["message"]["content"]
#
#     # === 15-word summary prompt ===
#     prompt_summary = (
#         "You are an expert in understanding logs and tell what is the log about so take these lines and Explain briefly the root cause of the issue in 20 words.\n"
#         "QUESTION: <your 20-word summary>"
#     )
#     full_prompt2 = f"{prompt_summary}\n{response_text}"
#     response2 = ollama.chat(model='llama3.2:latest', messages=[{"role": "user", "content": full_prompt2}])
#     summary_output = response2["message"]["content"]
#
#     question_match = re.search(r'QUESTION:\s*(.+)', summary_output)
#     question_only = question_match.group(1).strip() if question_match else summary_output.strip()
#
#     # === Firmware Extraction ===
#     firmware_match = re.search(r'Firmware version from file\s*:\s*\[([^\]]+)\]', file_content)
#     firmware_version = firmware_match.group(1).strip() if firmware_match else "Firmware version not available"
#
#     # === USERID Extraction ===
#     filename = os.path.basename(log_file)
#     userid_match = re.search(r"(?:log_)?([A-F0-9]{6,}(_\d+)?|\d+)", filename, re.IGNORECASE)
#     userid = userid_match.group(1) if userid_match else "unknown"
#
#     # === Timestamp from first NETWORK[INFO][netservice.c:net_service_thread] line ===
#     timestamp_pattern = r"([A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}\.\d{3})"
#     log_time = None
#     error_message = None
#
#     for line in file_content.split('\n'):
#         if "NETWORK[INFO][netservice.c:net_service_thread" in line:
#             match = re.search(timestamp_pattern, line)
#             if match:
#                 timestamp_str = match.group(1)
#                 try:
#                     timestamp_str_with_year = f"{datetime.now().year} {timestamp_str}"
#                     log_time = datetime.strptime(timestamp_str_with_year, "%Y %b %d %H:%M:%S.%f")
#                 except ValueError:
#                     log_time = None
#             error_message = line.strip()  # Save the entire line as the error message
#             break  # Only take the first occurrence
#
#     # === MAC Address Extraction ===
#     mac_pattern = r'(?:[0-9A-Fa-f]{12})'
#     mac_matches = re.findall(mac_pattern, file_content)
#     mac_address = mac_matches[0] if mac_matches else "MAC address not found"
#
#     file_type_value = "IOT logs"
#
#     # === Output Results ===
#     print(f"Processed file: {filename}")
#     print("USERID:", userid)
#     print("File Type:", file_type_value)
#     print("Question:\n", question_only)
#     print("Time:\n", f"{log_time} : {error_message}" if log_time and error_message else "No NETWORK timestamp found.")
#     print("MAC Address:\n", mac_address)
#     print("Firmware Version:\n", firmware_version)
#     print("-" * 50)