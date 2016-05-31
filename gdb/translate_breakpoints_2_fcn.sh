#!/bin/bash
# translate_brakpoints_fcn.sh - takes gdb.txt ("set logging on") and from the addresses of the 
# hit functions it looks up the function name in vmlinux_breakpoints.txt
# Input: gdb.txt and file_breakpoints.txt

GDB="$1"
DICT="$2"
ADDR_COL=3

while read line; do
    if [[ "$line" == *"??"* ]] ; then
       echo "$line" | cut -d " " -f $ADDR_COL >> hit_breakpoints
    fi
done < $GDB

#sed -i '$ d' hit_breakpoints # Used to deal with last line in file

while read address; do 
    while read line; do
        if [[ "$line" == *"break"* ]]; then 
            :
        else
            if [[ "$line" == *"$address"* ]]  ; then
                # sed -i -e 's/'$address'/'$line'' $BP
                echo "$line" >> list_hit_breakpoints
            fi
        fi
    done < "$DICT"
done < hit_breakpoints

