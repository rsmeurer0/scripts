#!/bin/bash
# set_disable_once.sh - Takes a list of breakpoints and disables every breakpoint once it is hit
# Input: list of breakpoints already in gdb format

FILE="$1"
n=0
sed -i -e 's/break \(\*0x[0-9a-f]*\).*/\0\n  commands\ndisable\ncontinue\n  end/' $FILE
while read line; do 
    string="disable"
    if [[ "$line" == "$string" ]] ; then
        n=$((++n))
        echo "$line" | sed -e 's/disable/disable '$n'/' >> selected_breakpoints_commands
    else
        echo "$line" >> selected_breakpoints_commands
    fi
done < $FILE
