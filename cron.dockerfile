FROM python:3.9-slim

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

# Install Cron
RUN apt-get update && apt-get install -y cron && which cron && \
    rm -rf /etc/cron.*/*

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

WORKDIR /app

COPY . .

# Run the command on container startup
ENTRYPOINT ["./run_cron.sh"]
