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
sudo apt-get install git ssh iperf tshark tcpdump nmap traceroute gpsd \
    gpsd-clients ircd-irc2 xchat python-geopy python-numpy python-pip \
    python-mysqldb python-mysql.connector mysql-server python-matplotlib \
    python-scipy python-netifaces libnl1
```

#### Download and install

Choose an appropriate directory and download the code from GitHub:
 
```
git clone https://github.com/contemmcm/atn-sim.git
```

Then, download and compile the necessary projects. Make sure to have installed the requirements described previously.

```
cd atn-sim
make all
sudo make install
```

##### Database configuration

First, you need to allow your MySQL server from other networks.

In Ubuntu 14.04, you can do so by editing the file `/etc/mysql/my.cnf`, changing the parameter bind-address to 0.0.0.0:

```
bind-address            = 0.0.0.0
```

Then, restart the MySQL server:

```
sudo service mysql restart
```

At this point, change to the `atn-sim/configs/db` directory and login  to MySQL server as super user. If you have defined a password for root user, add the option `-p` to the end of the following command.
```
mysql -u root
```

This would open a MySQL console.

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is xx
Server version: 5.5.52-0ubuntu0.14.04.1 (Ubuntu)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

Execute the following on the MySQL console:

```
create database atn_sim;
grant all privileges on atn_sim.* to atn_sim@'%' identified by 'atn_sim';
use atn_sim
source atn_sim.sql
exit
```

You are now ready to start the simulation.

## Quick Start

Initialize CORE:

```
sudo service core-daemon start
```

Open the graphical user interface for CORE by executing:

```
core-gui
```

Then, open an scenario file (e.g., sprint1.imn) and start the simulation by pressing the green arrow on the left menu.

Finally, initialize the ptracks, choosing a proper exercise (e.g., COREDEMO):

```
sudo service ptracks start COREDEMO
```