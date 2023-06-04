# https://hub.docker.com/_/python
FROM python:3.10-slim
ENV PYTHONUNBUFFERED True

# Install system dependencies
RUN apt-get update -y && apt-get install -y \
    tini \
    nfs-common \
    && apt-get clean

# Set fallback mount directory
ENV MNT_DIR /mnt/nfs/filestore

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Ensure the script is executable
RUN chmod +x /app/run.sh

# Use tini to manage zombie processes and signal forwarding
# https://github.com/krallin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# Pass the startup script as arguments to tini
CMD ["/app/run.sh"]
# [END cloudrun_fs_dockerfile]