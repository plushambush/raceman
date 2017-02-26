#!/bin/bash
echo $1 | nc -C 192.168.56.102 40040  > "$2.raw"
./convert.sh "$2.raw" "$2.wav"
rm "$2.raw"
