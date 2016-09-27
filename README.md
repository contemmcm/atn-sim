# atn-sim
Aeronautical Telecommunications Network (ATN) Simulator

## Installation

### Ubuntu 14.04

#### Requirements

##### Dump 1090
```
sudo apt-get install librtlsdr-dev librtlsdr0 rtl-sdr libusb-1.0-0-dev libusb-1.0-0
```

Please, refer to https://github.com/MalcolmRobb/dump1090 for more information on this project.

##### Common Open Research Emulator (CORE)
```
sudo apt-get install bash bridge-utils ebtables iproute libev-dev python tcl8.5 tk8.5 \
        libtk-img autoconf automake gcc make python-dev libreadline-dev pkg-config \
        imagemagick help2man python-sphinx
```

Please, refer to https://github.com/coreemu/core for more information on this project.

##### Extendable Mobile Ad-hoc Network Emulator (EMANE)
```
sudo apt-get install gcc g++ autoconf automake libtool libxml2-dev libprotobuf-dev \
    python-protobuf libpcap-dev libpcre3-dev uuid-dev libace-dev python-stdeb \
    debhelper pkg-config python-lxml python-setuptools protobuf-compiler
```

Please, refer to https://github.com/adjacentlink/emane for more information on this project.

##### Python Track Generator for Air Traffic Control (PTRACKS)
```
sudo apt-get install python-mpi4py python-qt4
```

Please, refer to https://github.com/contemmcm/ptracks for more information on this project.
 
##### General 
```
sudo apt-get install git subversion ssh iperf tshark tcpdump nmap traceroute \
    gpsd gpsd-clients ircd-irc2 xchat python-geopy python-numpy python-pip \
    python-mysqldb python-mysql.connector mysql-server python-matplotlib \
    python-scipy libnl1
```