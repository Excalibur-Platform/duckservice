#!/usr/bin/env bash
set -eo pipefail
mkdir -p $MNT_DIR

echo "Mounting Cloud Filestore - $FILESTORE_IP_ADDRESS:/$FILE_SHARE_NAME $MNT_DIR"
mount -o nolock $FILESTORE_IP_ADDRESS:/$FILE_SHARE_NAME $MNT_DIR
echo "Mounting completed."

exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app