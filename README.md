# Dusk-ITN2-Node-Height-Tracker

**Dusk ITN2 Node Height Tracker**

This is a python3 script that checks the node's status every minute and prints it to the console.

Original less featureful bash version still available. Instructions [here](https://github.com/Znomon/Dusk-ITN2-Node-Height-Tracker/blob/main/README_bash.md):

## Usage

1. Save the file `node_height_checker_w_estimate.py` to your computer that is running the node.

2. Run the script:
    ```bash
    python3 node_height_checker_w_estimate.py
    ```
## One-Liner

```bash
curl https://raw.githubusercontent.com/Znomon/Dusk-ITN2-Node-Height-Tracker/main/node_height_checker_w_estimate.py | python3
```

## Output Example

Output will look something like this:


```
Current Local Height: 78845
Current Global Height: 79989 (Age: 4 minutes)

Block Increase Over Time:
Interval (min)  Blocks Increased
1               139
5               641
15              983
30              1602
60              0

Estimated Time to Catch Up: 6 minutes, 4 seconds
```


## Notes

- The script only keeps track while it is running. As soon as you kill it, it loses all memory. You can re-run it, but it will only keep tracking since the start of the script.

- You can run it in the background by appending `&` to the end of the command like this:
    ```bash
    python3 node_height_checker_w_estimate.py &
    ```

    If you do this, it will run forever and print logs into the terminal seemingly from nowhere. You are not hacked. To kill the process, run:
    ```bash
    ps -ef | grep python
    ```

    You will see an output that looks like this:
    ```bash
    root         519       1  0 17:02 ?        00:00:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-s
    root         610       1  0 17:02 ?        00:00:00 /usr/bin/python3 /usr/share/unattended-upgrades/unatt
    user        3222    2612  0 17:48 pts/1    00:00:00 python3 node_height_checker_w_estimate.py
    user        3631    2612  0 18:21 pts/1    00:00:00 grep --color=auto python

    ```

    You will see a process with the script name in it. Find the leftmost number in the same line (in this example, it is 3222). You need to kill this process:
    ```bash
    kill 3222
    ```

## Disclaimer

This script is provided AS-IS.
