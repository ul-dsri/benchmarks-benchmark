#!/bin/sh

set -e  # Stop script execution on any unexpected error

# Set variables
NEW_HTML_FILE=$1
MC_ALIAS="${S3_ALIAS}"
S3_BUCKET="${S3_BUCKET}"
REMOTE_PATH="$MC_ALIAS/$S3_BUCKET/papers/benchmarks-benchmark/"

# Ensure the html file is provided
if [ -z "$NEW_HTML_FILE" ]; then
  echo "Usage: $0 <html-file>"
  exit 1
fi

# Ensure the html file exists
if [ ! -f "$NEW_HTML_FILE" ]; then
  echo "Error: HTML file '$NEW_HTML_FILE' not found."
  exit 1
fi

# Step 1: Compute the sha1sum of the new html file
COMPUTED_SHA1=$(sha1sum "$NEW_HTML_FILE" | awk '{print $1}')
echo "Computed sha1sum for new HTML file: $COMPUTED_SHA1"

# Step 2: Try downloading all HTML files from s3
mkdir -p ./tmp # make tmp dir if it doesn't already exist
echo "Downloading all HTML files from S3..."
if ! mc find $REMOTE_PATH --name "*.html" --exec "mc get {} ./tmp"; then
    echo "No HTML files found in S3. Continuing..."
fi
echo "Successfully checked and downloaded all HTML files (if any)"

# Step 3: Compare the computed sha1sum to the list
if find ./tmp -name "*.html" -exec sha1sum {} + | grep -q "$COMPUTED_SHA1"; then
  echo "SHA1sum found in the list. HTML file will not be uploaded."
  exit 0
fi

# Step 4: Upload the html file to S3
NEWFILEPATH="$(echo "$NEW_HTML_FILE" | sed -e 's/\.html$/_'$(date +%Y-%m-%d)'_'${CI_COMMIT_SHORT_SHA}'.html/g')"
cp "$NEW_HTML_FILE" "$NEWFILEPATH" # rename to include date and short commit
NEWFILE=$(basename "$NEWFILEPATH")
REMOTE_UPLOAD_PATH="$MC_ALIAS/$S3_BUCKET/papers/benchmarks-benchmark/$NEWFILE"

echo "Uploading html file to S3: $REMOTE_UPLOAD_PATH"
mc cp "$NEWFILEPATH" "$REMOTE_UPLOAD_PATH"
# Replace questionnaire.html with the latest version
mc cp "$NEW_HTML_FILE" "$MC_ALIAS/$S3_BUCKET/papers/benchmarks-benchmark/questionnaire.html"

# Step 5: Update questionnaire.csv
echo "Updating csv file in S3: $REMOTE_PATH/questionnaire.csv"
echo 'filename,url' > questionnaire.csv
mc ls "$REMOTE_PATH" -r | awk '{print $6}' | grep ".html$" | sed -e 's@.*@"&","https://dl.dsri.org/papers/benchmarks-benchmark/&"@g' >> questionnaire.csv
mc cp questionnaire.csv "$REMOTE_PATH/questionnaire.csv"
echo "questionnaire.csv uploaded successfully."

echo "questionnaire.html uploaded successfully."
exit 0

