#!/bin/bash

bash_script="/home/evan/autosnort.sh" 
python_script="/home/evan/parselog.py"  


while true; do
    # Run snort
    bash "$bash_script"
   

    # Parse ke influxdb
    python3 "$python_script"

 
done
