#!/bin/sh

set -e  # Stop script execution on any unexpected error

# Set variables
NEW_HTML_FILE=$1
MC_ALIAS="${S3_ALIAS}"
S3_BUCKET="${S3_BUCKET}"
REMOTE_PATH="$MC_ALIAS/$S3_BUCKET/papers/party-papers/"

# Ensure the html file is provided
if [ -z "$NEW_HTML_FILE" ]; then
  echo "Usage: $0 <html-file>"
  exit 1
fi

# Ensure the html file exists
if [ ! -f "$NEW_HTML_FILE" ]; then
  echo "conditional matched"
  ls -l "$NEW_HTML_FILE"
  ls -l $(realpath "$NEW_HTML_FILE")
  echo "Error: HTML file '$NEW_HTML_FILE' not found."
  exit 1
fi

# Step 1: Compute the sha1sum of the new html file
COMPUTED_SHA1=$(sha1sum "$NEW_HTML_FILE" | awk '{print $1}')
echo "Computed sha1sum for new HTML file: $COMPUTED_SHA1"

# Step 2: Try downloading all HTML files from s3
mkdir -p ./tmp # make tmp dir if it doesn't already exist
echo "Downloading all HTML files from S3..."
mc find $REMOTE_PATH --name "*.html" --exec "mc cp {} ./tmp"
echo "Successfully downloaded HTML files"

# Step 3: Compare the computed sha1sum to the list
if find ./tmp -name "*.html" -exec sha1sum {} + | grep "$COMPUTED_SHA1"; then
  echo "SHA1sum found in the list. HTML file will not be uploaded."
  exit 0
fi

# Step 4: Upload the html file to S3
NEWFILEPATH="$(echo "$NEW_HTML_FILE" | sed -e 's/\.html$/_'$(date +%Y-%m-%d)'_'${CI_COMMIT_SHORT_SHA}'.html/g')"
cp "$NEW_HTML_FILE" "$NEWFILEPATH" # rename to include date and short commit
NEWFILE=$(basename "$NEWFILEPATH")
REMOTE_UPLOAD_PATH="$MC_ALIAS/$S3_BUCKET/papers/party-papers/$NEWFILE"

echo "Uploading html file to S3: $REMOTE_UPLOAD_PATH"
mc cp "$NEWFILEPATH" "$REMOTE_UPLOAD_PATH"
# Replace questionnaire.html with the latest version
mc cp "$NEW_HTML_FILE" "$MC_ALIAS/$S3_BUCKET/papers/party-papers/questionnaire.html"

echo "Questionnaire uploaded successfully."
exit 0

