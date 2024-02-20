#!/bin/bash

# Define the intervals in minutes (including 1 minute)
intervals=(1 5 10 30 60)

# Function to get the current block height
get_current_height() {
    curl --silent --location --request POST 'http://127.0.0.1:8080/02/Chain' \
         --header 'Rusk-Version: 0.7.0-rc' \
         --header 'Content-Type: application/json' \
         --data-raw '{"topic": "gql", "data": "query { block(height: -1) { header { height } } }"}' | \
         jq -r '.block.header.height'
}

# Function to get the global block height
get_global_height() {
    height=$(curl --silent --max-time 10 'https://api.dusk.network/v1/latest?node=nodes.dusk.network' | jq -r '.data.blocks[0].header.height')
    if [[ "$height" =~ ^[0-9]+$ ]]; then
        echo "$height"
    else
        echo "failed"
    fi
}

# Initialize variables
declare -A history
global_height="Unavailable"
global_height_timestamp=$(date +%s)

# Main loop
while true; do
    current_height=$(get_current_height)
    current_time=$(date +%s)

    echo "Current Height: $current_height (Time: $(date -d @$current_time))"

    # Try to update global height every 5 minutes
    if (( current_time - global_height_timestamp >= 300 )); then
        new_global_height=$(get_global_height)
        if [[ "$new_global_height" != "failed" ]]; then
            global_height=$new_global_height
            global_height_timestamp=$current_time
        fi
    fi

    if [[ "$global_height" != "Unavailable" ]]; then
        age=$((current_time - global_height_timestamp))
        echo "Global Height: $global_height (Data age: $age seconds)"
    else
        echo "Global Height: Unavailable"
    fi

    # Store current height with timestamp
    history[$current_time]=$current_height

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
            if [[ $current_height =~ ^[0-9]+$ ]] && [[ $past_height =~ ^[0-9]+$ ]]; then
                increase=$((current_height - past_height))
                echo "Increase over last $interval minutes: $increase"
            else
                echo "Invalid data for calculation."
            fi
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
