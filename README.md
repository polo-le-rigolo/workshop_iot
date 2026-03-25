# Workshop IoT Hacking

## Overview

- [Intro](#intro)
    
- [Reconnaissance](#reconnaissance)
    
- [Hardware](#hardware)
    
- [Firmware](#firmware)
    
- [Troubleshooting](#Troubleshooting)

---

## Intro

Workshop Hardware GCC : getting your first root shell on a real device (UART, dumping and reversing firmware, finding vulnerabilities and exploiting them).

---

## Reconnaissance

- Debug headers on PCB,  labels on chips
   
- https://fccid.io/ (reports with internal photos)

- https://alldatasheet.com/ (to find datasheet of components)


---

## Hardware

### Identifying UART Pins

**Ground (GND)**

- Multimeter in continuity mode,   probe a known ground point (screw, shielding, antenna) 

**VCC (Power)**

- Power on the device  and look for constant voltage (3.3V or 5V)

**RX (Receive)**

- often around 0V (watch out as other chips might communicate over uart, not in our case)

**TX (Transmit)**

- Fluctuating voltage : multimeter may not detect it properly (sampling rate too low)  Using a logic analyzer or oscilloscope is a better option    
### Wiring

- GND ↔ GND
- RX ↔ TX
- TX ↔ RX
- ⚠️ Do NOT connect VCC 

### Commands

Find where the UART adapter is mounted :

```
ls /dev/tty*
```

Most of the time :

- `/dev/ttyUSB0`
- `/dev/ttyACM0`

Connect using a serial client :

```
sudo picocom -b BAUDRATE /dev/ttyUSB0
```

Alternatives:

- `minicom`
- `screen`
- `putty` (if you are a psychopath)

If you are running windows (shame on you), you can use a serial client like or use powershell to bind your serial port to a wsl device : 

```
usbipd-win
usbipd list
usbipd attach --wsl --busid=<BUSID>
```

---

### Boot Process

- Boot the device while connected (powercycle it if you missed the beggining) and copy the boot log into a txt file for further analysis : 
       
    - Debug messages
        
    - Credentials (sometimes)
        
    - Firmware/partition info (to unpack and repack firmware cleanly)
        
    - Bootloader access (e.g., failsafe mode)


---

## Firmware


## Troubleshooting

#### Problem 1 : I cannot see my uart to ttl adapter 

If you cannot find it or it doesn't seem to detect it's chinese cheap adapter so some might not work, I can give you another one but before check kernel logs (on windows you might have some drivers to install) :

```
dmesg
```

#### Problem 2 : I cannot see the boot log or I see only gibberish

If you don't see anything (you can connect to the serial adapter but nothing is showing up even after powercycling the device), then it means your wiring is wrong. 
Try swapping RX and TX.

If you see some output but it looks corrupted / incomplete then it's most likely your baudrate that's wrong. 
 
Try common baud rates: `115200`, `57600`, `38400`
