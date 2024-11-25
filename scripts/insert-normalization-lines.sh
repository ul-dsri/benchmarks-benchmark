#!/bin/bash

# Ensure the script is called with a filename
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

FILE="$1"

# Use sed to insert the lines as the 2nd and 3rd lines
sed -i '2i\% Add metadata suppression\n\\pdfinfoomitdate=1\n\\pdftrailerid{}' "$FILE"

echo "Added lines to $FILE"

