#!/bin/bash
sox  -r 22k -t raw -e signed-integer -b 16 -c 2 $1 -t ogg -r 8k -c 1  $2