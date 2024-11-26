#!/bin/bash

# Ensure the script is called with a filename
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

FILE="$1"

# Ensure the file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File $FILE does not exist."
    exit 1
fi

# Use sed to remove the normalization lines
sed -i '/% Add metadata suppression/d' "$FILE"
sed -i '/\\pdfinfoomitdate=1/d' "$FILE"
sed -i '/\\pdftrailerid{}/d' "$FILE"

echo "Removed lines from $FILE"

