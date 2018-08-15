#!/bin/bash
BLACKMAGIC=(/dev/serial/by-id/usb-Black_Sphere_Technologies_Black_Magic_Probe_*-if00)
TARGETPWR="disable"

show_help() {
cat << EOF
Usage: ${0##*/} [-ht] [-d DEVICE] FIRMWARE
Flash a firmware image using the Black Magic JTAG probe.

     -h          display this help and exit
     -t          provide target power from the JTAG probe
     -d DEVICE   connect to a JTAG probe at DEVICE
EOF
}

## Parse arguments
OPTIND=1
while getopts htd: OPT; do
   case $OPT in
      h)
         show_help
         exit 0
         ;;
      t)
         TARGETPWR="enable"
         ;;
      d)
         BLACKMAGIC=$OPTARG
         ;;
      *)
         show_help >&2
         exit 1
         ;;
   esac
done
shift $((OPTIND - 1))

## Must provide a firmware image
if [ "$#" -eq "0" ]; then
   echo "Missing argument: FIRMWARE" >&2
   show_help >&2
   exit 1
fi
FIRMWARE=$1
shift 1
if [ ! -r "$FIRMWARE" ]; then
    echo "Firmware image '$FIRMWARE' is not readable" >&2
    exit 1
fi

## Run GDB to load the firmware
gdb-multiarch -n -q --exec=${FIRMWARE} << EOF
target extended-remote ${BLACKMAGIC}
monitor tpwr ${TARGETPWR}
monitor swdp_scan
attach 1
monitor erase
load
detach
EOF
echo
