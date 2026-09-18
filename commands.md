## CAN

sudo modprobe can
sudo modprobe slcan
sudo modprode can_raw

sudo slcand -l -c -s6 /dev/ttyACM0 can0

sudo ip link set can0 up

candump can0

## VCAN

sudo modprode vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up

canplayer -I candump-2026-09-12_152132.log vcan0=can0
