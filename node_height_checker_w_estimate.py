import requests
import time
from datetime import datetime, timedelta
import subprocess
import json

def count_blocks_mined():
    # Run the grep command and capture its output
    grep_process = subprocess.Popen(["grep", "execute_state_transition", "/var/log/rusk.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = grep_process.communicate()

    # Count the number of lines returned by the grep command
    num_lines = len(output.decode().split('\n')) - 1

    # Check if the number of lines increased since the last call
    if hasattr(count_blocks_mined, 'last_count'):
        if num_lines > count_blocks_mined.last_count:
            print("####### BLOCK MINED! #######")

    # Update the last count value
    count_blocks_mined.last_count = num_lines

    return num_lines

def check_consensus_keys_password():
    # Define the number of lines to check at the end of the log file
    num_lines_to_check = 2000

    # Run the tail command to get the last 2000 lines of the log file
    tail_process = subprocess.Popen(["tail", "-n", str(num_lines_to_check), "/var/log/rusk.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = tail_process.communicate()

    # Convert the output from bytes to a string
    log_data = output.decode()

    # Check for the specific error message in the log data
    if "Invalid consensus keys password: BlockModeError" in log_data:
        print("ERROR: Invalid consensus keys password detected. Please ensure you have entered the correct password. Refer to the steps on the website (https://docs.dusk.network/itn/node-running-guide/) for guidance.")

def dusk_network_connect_status():
    # Run the tail command to get the last 500 lines of the log file
    tail_process = subprocess.Popen(["tail", "-n", "50", "/var/log/rusk.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = tail_process.communicate()

    # Check for the string "block received" in the output
    if "block received" in output.decode():
        status = "Connected"
    else:
        status = "NOT Connected"

    print(f"DUSK Network Status: {status}")

def get_current_local_height():
    response = requests.post(
        'http://127.0.0.1:8080/02/Chain',
        headers={'Rusk-Version': '0.7.0-rc', 'Content-Type': 'application/json'},
        json={"topic": "gql", "data": "query { block(height: -1) { header { height } } }"}
    )
    return response.json()['block']['header']['height']

def get_global_height():
    response = requests.get('https://api.dusk.network/v1/latest?node=nodes.dusk.network', timeout=2)
    data = response.json()
    # Check if 'data' key exists in the response
    if 'data' in data and 'blocks' in data['data'] and len(data['data']['blocks']) > 0:
        return data['data']['blocks'][0]['header']['height']
    else:
        # Handle the absence of 'data' or 'blocks' key
        raise KeyError("Key 'data' or 'blocks' not found in the response")

def get_global_height_safe(): #this needs a thread
    try:
        global_height = get_global_height()
        return global_height, datetime.now()
    except requests.exceptions.Timeout:
        print("Block Explorer timed out, retrying...")
        #time.sleep(10)
    except KeyError as e:
        print("Server Error from Block Explorer, retrying later...")
        #time.sleep(10)

    return None, datetime.now()

def calculate_block_increase(local_heights, interval, current_height):
    if len(local_heights[interval]) >= 2:
        return current_height - local_heights[interval][-2]
    return 0

def format_timedelta(td):
    days = td.days
    hours, rem = divmod(td.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days} days")
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minutes")
    if seconds:
        parts.append(f"{seconds} seconds")

    return ", ".join(parts)

def main():
    intervals = [1, 5, 15, 30, 60]  # Minutes
    local_heights = {interval: [] for interval in intervals}
    last_interval_check = {interval: datetime.now() for interval in intervals}

    # Get initial local height
    local_height = get_current_local_height()
    global_height, last_global_check = get_global_height_safe()

    check_consensus_keys_password()

    while True:
        current_time = datetime.now()

        # Update local heights for each interval
        for interval in intervals:
            time_since_last_interval_check = (current_time - last_interval_check[interval]).total_seconds()
            if time_since_last_interval_check >= interval * 60 or not local_heights[interval]:
                local_heights[interval].append(local_height)
                if len(local_heights[interval]) > 2:
                    local_heights[interval].pop(0)  # Keep only the last two records
                last_interval_check[interval] = current_time

        # Update local height for the next iteration
        local_height = get_current_local_height()

        # Display local height
        print("-----------------------------")
        print("\nCurrent Local Height:", local_height)

        # Update and handle global height information
        if (current_time - last_global_check).total_seconds() >= 300:
            global_height, last_global_check = get_global_height_safe()

        # Display global height
        if global_height is not None:
            age = datetime.now() - last_global_check
            age_text = "Now" if age.total_seconds() < 1 else format_timedelta(age)
            print(f"Current Global Height: {global_height} (Age: {age_text})")
        else:
            print("Current Global Height: Unavailable")

        # Display blocks mined
        print("Blocks Mined:", count_blocks_mined())
        dusk_network_connect_status()
        # Display interval block increase information
        print("\n-----------------------------")
        print("\nBlocks seen per 'X' minutes:")
        print("Interval (min)\tBlocks Increased")
        for interval in intervals:
            blocks_increased = calculate_block_increase(local_heights, interval, local_height)
            print(f"{interval}\t\t{blocks_increased}")

        if global_height is not None:
            # Calculate estimated catch-up time using the largest available interval
            estimated_catch_up_time = None
            for interval in reversed(intervals):
                blocks_behind = global_height - local_height
                blocks_per_interval = calculate_block_increase(local_heights, interval, local_height)
                if blocks_per_interval > 0:
                    time_per_block = interval * 60 / blocks_per_interval
                    total_time_seconds = time_per_block * blocks_behind
                    estimated_catch_up_time = timedelta(seconds=total_time_seconds)
                    break

            if estimated_catch_up_time:
                # Check if the estimated catch-up time is negative or zero
                if estimated_catch_up_time.total_seconds() <= 0:
                    print("\nEstimated Time to Catch Up: SYNCED!")
                else:
                    print("\nEstimated Time to Catch Up:", format_timedelta(estimated_catch_up_time))

        time.sleep(60)  # Wait for 1 minute before next check

if __name__ == "__main__":
    main()
