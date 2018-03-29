#!/bin/bash
count=0

while :
do
  ssh bw python resub.py
  count=$((count+1))
  echo "job manager running successfully for "$count" steps, going to sleep"
  sleep 1800
done
