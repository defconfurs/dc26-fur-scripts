#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
SERIALNO=$1
SERIALBIN=$(mktemp --suffix=.bin)

function atexit {
   rm $SERIALBIN
}

## Write the serial number - in little endian
SERHI=$(((SERIALNO >> 8) & 0xff))
SERLO=$(((SERIALNO >> 0) & 0xff))
printf "%02x %02x 26 dc" $SERLO $SERHI | xxd -p -r > $SERIALBIN

## Pad with random data to fill out a 256-bit block
dd if=/dev/urandom bs=28 count=1 2>/dev/null >> $SERIALBIN

## Program the OTP region
dfu-util -a 2 -d 0483:df11 -s 0x1FFF7800 -D $SERIALBIN
## Lock the OTP region
dfu-util -a 2 -d 0483:df11 -s 0x1FFF7A00 -D ${DIR}/lock0.bin
