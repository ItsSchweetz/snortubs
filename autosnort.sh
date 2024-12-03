#!/bin/bash

# Paths and configurations
snort_cmd="sudo snort -i enp0s3 -c /etc/snort/snort.conf -l /var/log/snort -d -A console"
output_file="/home/evan/sti.txt"
alert_bot_script="/home/evan/alertbot.sh"  # Adjust this path to where your alertbot.sh script is located


    # Run Snort and redirect output to sti.txt in the background
    echo "Starting Snort..."
    $snort_cmd > "$output_file" &  # Redirecting the output to sti.txt
    snort_pid=$!  # Capture the PID of the Snort process

    # Allow Snort to run for a moment
    sleep 5

    # Kill Snort
    echo "Stopping Snort..."
    sudo kill "$snort_pid"  # Ensure you have sudo permissions
    wait "$snort_pid" 2>/dev/null  # Wait for the Snort process to terminate

    # Run alertbot.sh to process the output file in the background
    echo "Starting alertbot.sh..."
    bash "$alert_bot_script" &
    alert_bot_pid=$!  # Capture the PID of the alertbot process

    # Allow alertbot.sh to run for a moment
    sleep 5

    # Kill alertbot.sh
    echo "Stopping alertbot.sh..."
    kill "$alert_bot_pid"
    wait "$alert_bot_pid" 2>/dev/null  # Wait for the alertbot process to terminate

    # Optional: Allow a moment for cleanup
    #sleep 1

