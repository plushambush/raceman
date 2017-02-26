#!/bin/bash
sox  -r 22k -t raw -e signed-integer -b 16 -c 2 $1 -t wav -r 22k -b 16 -c 2 -e signed-integer $2