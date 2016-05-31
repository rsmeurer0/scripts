#!/bin/bash
#insert the continue command afet the break point in order to get a full list of hitten breakpoints

FILE="$1"

sed -i -e 's/break \(\*0x[0-9a-f]*\).*/\0\n  commands\ncontinue\n  end/' $FILE


