# Dusk-ITN2-Node-Height-Tracker

**Dusk ITN2 Node Height Tracker**

This is a shell script that checks the node's status every minute and prints it to the console.

## Usage

1. Save the file `dusk_node_height_checker.sh` to your computer that is running the node.

2. Make the file executable:
    ```bash
    chmod +x dusk_node_height_checker.sh
    ```

3. Run the script:
    ```bash
    ./dusk_node_height_checker.sh
    ```

## Output Example

Output will look something like this:



```
Current Height: 68940 (Time: Tue Feb 20 01:39:55 PM EST 2024)
Increase over last 1 minutes: 32
Increase over last 5 minutes: 95
No data for full 10 minute interval yet.
No data for full 30 minute interval yet.
No data for full 60 minute interval yet.
```


## Notes

- The script only keeps track while it is running. As soon as you kill it, it loses all memory. You can re-run it, but it will only keep tracking since the start of the script.

- You can run it in the background by appending `&` to the end of the command like this:
    ```bash
    ./dusk_node_height_checker.sh &
    ```

    If you do this, it will run forever and print logs into the terminal seemingly from nowhere. You are not hacked. To kill the process, run:
    ```bash
    ps -ef | grep height
    ```

    You will see an output that looks like this:
    ```bash
    user       3178    2227  0 13:34 pts/0    00:00:00 /bin/bash ./dusk_node_height_checker.sh
    user       3233    2227  0 13:42 pts/0    00:00:00 grep --color=auto height
    ```

    You will see a process with the script name in it. Find the leftmost number in the same line (in this example, it is 3178). You need to kill this process:
    ```bash
    kill 3178
    ```

## Disclaimer

This script is provided AS-IS.
