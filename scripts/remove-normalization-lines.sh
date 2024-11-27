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

# Count the number of lines in the file before removal
LINE_COUNT_BEFORE=$(wc -l < "$FILE")

# Use sed to remove the exact block of lines previosly added
sed -i '/^% Add metadata suppression$/ {N;N; /^% Add metadata suppression\n\\pdfinfoomitdate=1\n\\pdftrailerid{}$/d; }' "$FILE"

# Count the number of lines in the file after removal
LINE_COUNT_AFTER=$(wc -l < "$FILE")

# Check if the line count difference is exactly 3
if [ $((LINE_COUNT_BEFORE - LINE_COUNT_AFTER)) -ne 3 ]; then
    echo "Error: The file does not have exactly a 3-line difference."
    echo "Either the file had multiple instances of the block, or did not contain the block"
    exit 1
fi

echo "Removed lines from $FILE"

