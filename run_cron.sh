#!/bin/sh

echo "ASYLUM_WEB_CONFIG=$ASYLUM_WEB_CONFIG" >> /etc/environment

exec cron -f -l 2

