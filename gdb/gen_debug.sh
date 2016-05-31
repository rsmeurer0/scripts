#!/bin/bash
#
#
#
# Usager: 

FILE="$1" # Target ELF, in our case is vmlinux
LIST="$2" # functions_of_interest.txt - Must be the file with this exact name
DISABLE="$3" # yes, if the user wants to disable all of the breakpoints when hit
# which contains parts of function names that will be filtered

if [ "$#" -ge 2 ] ; then

    echo "Generating the Breakpoints from ELF"
    ./gen_breakpoints.sh $FILE

    echo "Filtering functions from file"
    ./gen_breakpoints.py $LIST vmlinux_breakpoints.txt

    echo "Generating Object Dump from ELF"
    objdump -S $FILE > kernel_dump

    if [ "$#" -eq 3 ] ; then

        if [[ "$DISABLE" == "yes" ]] ; then
            echo "Adding Commands to disable breakpoints after hit"
            ./set_disable_once.sh selected_breakpoints.txt
        fi

    fi
fi


