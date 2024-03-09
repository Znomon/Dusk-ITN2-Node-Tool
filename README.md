
# Dusk Node Tookit

## **Stop being a monkey with a typewriter! Let computers do the work for you!**

For anyone else obsessively checking their node sync status with those curl commands and grepping log files. 
**It stops here.**

## Features:
- Checks for some common bugs like Network Connectivity and consensus key password
- Reports # of blocks 'mined' and when the last one happened
- Sync status/progress indicator

# Instructions:
Copy paste this to node
```
curl --silent https://raw.githubusercontent.com/Znomon/Dusk-ITN2-Node-Tool/main/node_height_checker_w_estimate.py | python3
```

## Example Output:
```-----------------------------
Your Local Node Block Height: 340270
Estimated Global Block Height: 340250 (Age: 1 minutes)
Node Status: SYNCED!
Total Blocks Mined: 242 (Last mined 12 minutes ago)
DUSK Network Status: ONLINE - Connected to 100 Nodes
-----------------------------
Blocks 'accepted' in the last 1 minutes: 5
Blocks 'accepted' in the last 5 minutes: 47
Blocks 'accepted' in the last 15 minutes: 103
```

# ERRORS:
if you see this error ```ModuleNotFoundError: No module named 'requests'``` Run this: ```sudo apt-get update
sudo apt-get install python3-requests```

UPDATE 8: Changed API call per Dev's request. 
Added a check for archived log files. 

-----------------------------------------------------
ALWAYS be aware of people trying to scam you in crypto. 
ALWAYS be suspicious of people asking you to run code on your computer
This script is provided open source for this reason.
https://github.com/Znomon/Dusk-ITN2-Node-Tool

## Disclaimer

This script is provided AS-IS.
