#!/bin/bash

# Define the intervals in minutes
intervals=(5 10 30 60)

# Function to get the current block height
get_current_height() {
    curl --silent --location --request POST 'http://127.0.0.1:8080/02/Chain' \
         --header 'Rusk-Version: 0.7.0-rc' \
         --header 'Content-Type: application/json' \
         --data-raw '{"topic": "gql", "data": "query { block(height: -1) { header { height } } }"}' | \
         jq -r '.block.header.height'
}

# Initialize an associative array to store historical values
declare -A history

# Main loop
while true; do
    current_height=$(get_current_height)
    current_time=$(date +%s)

    # Store current height with timestamp
    history[$current_time]=$current_height

    echo "Current Height: $current_height (Time: $(date -d @$current_time))"

    # Check for increases over defined intervals
    for interval in "${intervals[@]}"; do
        past_time=$((current_time - interval * 60))
        closest_time=0
        for time in "${!history[@]}"; do
            if (( time <= past_time && time > closest_time )); then
                closest_time=$time
            fi
        done
        if [ $closest_time -ne 0 ]; then
            past_height=${history[$closest_time]}
            increase=$((current_height - past_height))
            echo "Increase over last $interval minutes: $increase"
        else
            echo "No data for full $interval minute interval yet."
        fi
    done

    echo "-------------------------------------"

    # Cleanup: remove data older than 60 minutes
    for time in "${!history[@]}"; do
        if (( time < current_time - 3600 )); then
            unset history[$time]
        fi
    done

    # Sleep for a defined interval before next check
    sleep 60
done
