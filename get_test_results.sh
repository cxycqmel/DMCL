#!/bin/bash

for dir in `ls checkpoints`; do 
  if [ -e  checkpoints/$dir/test_metrics.txt ] && [ -e checkpoints/$dir/metrics.txt ]; then
    echo "dir name: "$dir;  
    python get_test_results.py checkpoints/$dir/test_metrics.txt checkpoints/$dir/metrics.txt;
    echo "" 
  fi
done
