import re
import csv

fpath = "smtp6.txt"
fdata_save = "smtp_6.csv"


timestamp_pattern = re.compile(r"^(\w+\s+\d+\s+\d+:\d+:\d+)")
msgid_pattern = re.compile(r"([A-F0-9]{10,}):")
from_pattern = re.compile(r"from=<([^>]+)>")
to_pattern = re.compile(r"to=<([^>]+)>")
status_pattern = re.compile(r"status=(\w+)")


msg_from = {}  
records = []   

with open(fpath, 'r') as logfile:
    for line in logfile:
        line = line.strip()
        if not line:
            continue

        timestamp_match = timestamp_pattern.search(line)
        msgid_match = msgid_pattern.search(line)
        if not msgid_match:
            continue

        msg_id = msgid_match.group(1)
        timestamp = timestamp_match.group(1) if timestamp_match else ""

        # Map sender from qmgr lines
        if "postfix/qmgr" in line:
            from_match = from_pattern.search(line)
            if from_match:
                msg_from[msg_id] = from_match.group(1)

        # Map recipient and status from smtp lines
        if "postfix/smtp" in line:
            to_match = to_pattern.search(line)
            status_match = status_pattern.search(line)
            if to_match:
                records.append({
                    'timestamp': timestamp,
                    'msg_id': msg_id,
                    'from': msg_from.get(msg_id, ""),  
                    'to': to_match.group(1),
                    'status': status_match.group(1) if status_match else ""
                })


with open(fdata_save, 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'msg_id', 'from', 'to', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for record in records:
        writer.writerow(record)

print(f"Parsing complete! Output saved to {fdata_save}")