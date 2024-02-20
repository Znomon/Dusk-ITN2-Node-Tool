# Dusk-ITN2-Node-Height-Tracker
Dusk ITN2 Node Height Tracker

Shell script that checks the node's status every minute and prints to console

Save the file to your computer that is running the node. Run the following command to allow it to run. 

chmod +x dusk_node_height_checker.sh

then run the script. 

./dusk_node_height_checker.sh

output will look something like this

-------------------------------------
Current Height: 68940 (Time: Tue Feb 20 01:39:55 PM EST 2024)
Increase over last 1 minutes: 32
Increase over last 5 minutes: 95
No data for full 10 minute interval yet.
No data for full 30 minute interval yet.
No data for full 60 minute interval yet.
-------------------------------------

It only keeps track while it is running. as soon as you kill it, it loses all memory. You can re-run it. but it will only keep tracking since the start of the script.

You can run it in the background by appending & to the end of the command like this. 

./dusk_node_height_checker.sh & 

if you do this it will run forever and spit out logs into the terminal seeminly from nowhere. No you arent hacked. Kill the process like this.

Run this command
ps -ef | grep height

you will see something like this.
user       3178    2227  0 13:34 pts/0    00:00:00 /bin/bash ./dusk_node_height_checker.sh
user       3233    2227  0 13:42 pts/0    00:00:00 grep --color=auto height


You will see a process with the script name in it. Find the leftmost number in the same line, in this example it is 3178. You need to kill this process.

kill 3178

Thats all. This is provided AS-IS
