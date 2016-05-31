#!/bin/bash
#
#
#
# Usage: sudo ./do_all.sh vmlinux functions_of_interest.txt (yes)  - Args inside () are optional

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi


FILE="$1" # usually vmlinux in this script, but can also apply to any non-stripped ELF inside a virtual disk
LIST="$2" # functions_of_insterest.txt - Must be a file with this exact name with the function names
DISABLE="$3" # Yes if you want to set all the breakpoints to automatic mode

if [ "$#" -eq 3 ] ; then
    virt-copy-out -a ../alpine.qcow /root/lisha-dev/linux-3.18.20/${FILE} .
    echo "Got File From Virtual Disk"

    if [ -f "$FILE" ]; then
        echo "Generating Breakpoints"
        ./gen_breakpoints.sh $FILE

        echo "Filtering Breakpoints"
        ./gen_breakpoints.py $LIST ${FILE}_breakpoints.txt

        if [[ "$DISABLE" == "yes" ]] ; then
            echo "Adding Commands"
            ./set_disable_once.sh selected_breakpoints.txt
        fi
        
        echo "Generating Object Dump"
        objdump -S $FILE > objdump_list
    fi
fi
