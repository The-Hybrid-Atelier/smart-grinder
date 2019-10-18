# smart-grinder
Repo for microphone glass grinder setup. 

## Requirements
* Python 3

## Installation 
`pip3 install pyserial`
`pip3 install matplotlib`
`pip3 install drawnow`

## Run Instructions

`python3 mic_listen.py -u 100 -p \dev\tty.usbmodem123`

Flags: 
* -u: user_id --> saves data to "/user_id.txt"
* -p: port


File Format: 
ln 1: timestamp (epoch)
ln 2: first_sample
ln n: n-th_sample


Author: Hedieh Moradi
Date: 10 Oct 2019
