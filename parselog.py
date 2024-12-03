import re
from datetime import datetime
from influxdb import InfluxDBClient

# Set up InfluxDB client
client = InfluxDBClient(host='localhost', port=8086, database='snort')

def parse_snort_log(log_file):
    print("Script started.")
    print(f"Opening log file: {log_file}")

    # Define the regex pattern for parsing log lines without nanoseconds
    log_pattern = re.compile(
        r'^(?P<timestamp>\d{2}/\d{2}-\d{2}:\d{2}:\d{2})\.\d+  \[\*\*\] \[(?P<alert_id>[^\]]+)\] (?P<alert_message>.*?) \[\*\*\] \[Priority: (?P<priority>\d+)\] \{(?P<protocol>\w+)\} (?P<source_ip>\S+) -> (?P<destination_ip>\S+)$'
    )

    try:
        with open(log_file, 'r') as f:
            print("File opened successfully.")
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    print(f"Line {line_number}: Empty line. Skipping.")
                    continue

                print(f"Line {line_number}: Processing line: {line}")

                match = log_pattern.match(line)
                if not match:
                    print(f"Line {line_number}: Line does not match the expected format. Skipping.")
                    continue

                # Extract fields using named groups
                timestamp_raw = match.group('timestamp')  # e.g., '10/08-13:38:16'
                alert_id = match.group('alert_id')        # e.g., '1:10000001:1'
                alert_message = match.group('alert_message')  # e.g., 'Ping Test'
                priority = match.group('priority')        # e.g., '0'
                protocol = match.group('protocol')        # e.g., 'ICMP'
                source_ip = match.group('source_ip')      # e.g., '192.168.199.164'
                destination_ip = match.group('destination_ip')  # e.g., '192.168.199.167'

                print(f"Line {line_number}: Extracted Data - Timestamp: {timestamp_raw}, Alert ID: {alert_id}, Alert Message: {alert_message}, Priority: {priority}, Protocol: {protocol}, Source IP: {source_ip}, Destination IP: {destination_ip}")

                # Append current year to the timestamp for accurate parsing
                current_year = datetime.now().year
                timestamp_with_year = f"{current_year}/{timestamp_raw}"  # e.g., '2024/10/08-13:38:16'

                # Parse the timestamp to remove any fractional seconds
                try:
                    parsed_time = datetime.strptime(timestamp_with_year, "%Y/%m/%d-%H:%M:%S")
                    alert_time = parsed_time.strftime("%Y-%m-%dT%H:%M:%S")  # Convert to ISO format without fractional seconds
                    print(f"Line {line_number}: Parsed timestamp (ISO format): {alert_time}")
                except ValueError as e:
                    print(f"Line {line_number}: Error parsing timestamp: {timestamp_with_year}, Error: {e}")
                    continue

                # Create the data point for InfluxDB
                alert_data = {
                    "measurement": "snort_alerts",
                    "tags": {
                        "source_ip": source_ip,
                        "destination_ip": destination_ip,
                        "alert_id": alert_id,
                        "alert_message": alert_message,
                        "protocol": protocol
                    },
                    "fields": {
                        "count": 1
                    },
                    "time": alert_time
                }

                print(f"Line {line_number}: Attempting to write data to InfluxDB: {alert_data}")

                # Attempt to write to InfluxDB with correct time precision
                try:
                    success = client.write_points([alert_data])
                    if success:
                        print(f"Line {line_number}: Data written to InfluxDB.")
                    else:
                        print(f"Line {line_number}: Failed to write data to InfluxDB.")
                except Exception as e:
                    print(f"Line {line_number}: Error writing to InfluxDB: {e}")

    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Call the function with your Snort log file path
parse_snort_log('/home/evan/sti.txt')  # Adjust the path as necessary.
