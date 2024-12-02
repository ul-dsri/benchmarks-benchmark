#!/bin/sh

set -e  # Stop script execution on any unexpected error

# Set variables
NORMALIZED_FILE=$1
MC_ALIAS="${S3_ALIAS}"
S3_BUCKET="${S3_BUCKET}"
SHA1_LIST_FILE="sha1sums.txt"
LOCAL_SHA1_LIST="/tmp/$SHA1_LIST_FILE"
REMOTE_PATH="$MC_ALIAS/$S3_BUCKET/$SHA1_LIST_FILE"
FLAG_FILE="uploaded_true"

# Ensure the normalized file is provided
if [ -z "$NORMALIZED_FILE" ]; then
  echo "Usage: $0 <normalized-file>"
  exit 1
fi

# Derive the non-normalized file name
if [[ "$NORMALIZED_FILE" == *_normalized.pdf ]]; then
  FILE_TO_UPLOAD="${NORMALIZED_FILE%_normalized.pdf}.pdf"
else
  echo "Error: File name must end with '_normalized.pdf'."
  exit 1
fi

# Ensure the non-normalized file exists
if [ ! -f "$FILE_TO_UPLOAD" ]; then
  echo "Error: Non-normalized file '$FILE_TO_UPLOAD' not found."
  exit 1
fi

# Step 1: Compute the sha1sum of the normalized file
COMPUTED_SHA1=$(sha1sum "$NORMALIZED_FILE" | awk '{print $1}')
echo "Computed sha1sum for normalized file: $COMPUTED_SHA1"

# Step 2: Try downloading the sha1sum list from S3
echo "Attempting to download sha1sum list from S3..."
if mc cp "$REMOTE_PATH" "$LOCAL_SHA1_LIST"; then
  echo "Successfully downloaded sha1sum list."
else
  echo "SHA1 list not found in S3. Proceeding with an empty list."
  > "$LOCAL_SHA1_LIST"  # Create an empty sha1sum list file
fi

# Step 3: Compare the computed sha1sum to the list
if grep -q "$COMPUTED_SHA1" "$LOCAL_SHA1_LIST"; then
  echo "SHA1sum found in the list. File will not be uploaded."
  exit 0
else
  echo "SHA1sum not found in the list. Appending it to the list."
  echo "$COMPUTED_SHA1" >> "$LOCAL_SHA1_LIST"
fi

# Step 4: Upload the non-normalized file to S3
NEWFILEPATH="$(echo "$FILE_TO_UPLOAD" | sed -e 's/\.pdf$/_'$(date +%Y-%m-%d)'_'${CI_COMMIT_SHORT_SHA}'.pdf/g')"
cp "$FILE_TO_UPLOAD" "$NEWFILEPATH" # rename to include date and short commit
NEWFILE=$(basename "$NEWFILEPATH")
REMOTE_UPLOAD_PATH="$MC_ALIAS/$S3_BUCKET/$NEWFILE"

echo "Uploading non-normalized file to S3: $REMOTE_UPLOAD_PATH"
mc cp "$NEWFILEPATH" "$REMOTE_UPLOAD_PATH"

# Step 5: Upload the updated sha1sum list back to S3
echo "Uploading updated sha1sum list to S3..."
mc cp "$LOCAL_SHA1_LIST" "$REMOTE_PATH"

# Create uploaded flag file
touch $FLAG_FILE

echo "File uploaded and sha1sum list updated successfully."
exit 0

