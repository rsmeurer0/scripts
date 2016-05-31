#!/bin/bash
# Create a list of the function names and also a list of breakpoints of these functions to be used in GDB

FILE="$1"

nm $FILE | egrep ' [TW] ' > ${FILE}FunctionIndex 
sed -i -e 's/^/0x/' ${FILE}FunctionIndex

nm $FILE | egrep ' [TW] ' | grep -Eo '^[^ ]+' > ${FILE}ListOfBreakpoints
sed -i -e 's/^/break *0x/' ${FILE}ListOfBreakpoints
sed -i '/break/a  commands\n    continue\n  end' ${FILE}ListOfBreakpoints

mv ${FILE}ListOfBreakpoints .
mv ${FILE}FunctionIndex .
