#!/bin/bash

# Start the first process
python analysis.py &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start the analysis process: $status"
  exit $status
fi
