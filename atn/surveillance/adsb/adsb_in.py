import ConfigParser
import logging
import os
import socket
import time

from .forwarders import dump1090_fwrd


class AdsbIn:

    net_port = 30001

    def __init__(self, config="adsbin.cfg"):
        self.logger = logging.getLogger('adsb_in_app.AdsBIn')

        # List of destination to which received messages will be forwarded to.
        self.forwarders = []

        # Id
        self.id = None

        if os.path.exists(config):
            conf = ConfigParser.ConfigParser()
            conf.read(config)

            self.id = conf.get("General", "id")

            # Reading destinations to forward received messages
            for dst in conf.get("General", "destinations").split():
                items = conf.items(dst)
                d = {}

                for i in items:
                    d[i[0]] = i[1]

                if d["type"] == "dump1090":
                    f = dump1090_fwrd.Dump1090Forwarder(items=d)
                    f.set_timeout(0.5)
                    self.forwarders.append(f)
                #elif d["type"] == "mysql":
                #    f = MysqlForwarder(verbose=verbose, items=d, sensor_id=self.id_sensor)
                #    self.forwarders.append(f)
                #elif d["type"] == "asterix":
                #    f = AsterixForwarder(verbose=verbose, items=d)
                #    self.forwarders.append(f)

    def start(self):
        print "  ,---.  ,------.   ,---.        ,-----.          ,--.         "
        print " /  O  \ |  .-.  \ '   .-',-----.|  |) /_         |  |,--,--,  "
        print "|  .-.  ||  |  \  :`.  `-.'-----'|  .-.  \        |  ||      \ "
        print "|  | |  ||  '--'  /.-'    |      |  '--' /        |  ||  ||  | "
        print "`--' `--'`-------' `-----'       `------'         `--'`--''--' "

        # Create a socket for receiving ADS-B messages
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', self.net_port))

        self.logger.info("Waiting on port :" + str(self.net_port))

        while True:
            # Buffer size is 1024 bytes
            data, addr = sock.recvfrom(1024)

            # Time of arrival
            toa = time.time()

            print (addr, data, toa)

            # ADSB-Out transmits message, nemid and node name.
            # NEM id and node name are used to calculate a precise time of arrival (TOA)
            # message, nodename, nemid = data.split()
            #message, lat_tx, lon_tx, alt_tx = data.split()
            message = data

            # Fix time of arrival for MLAT purposes
            # if self.TOA_SIMULATED:
            #    toa, x, y, z = self.calc_propagation_time(float(lat_tx), float(lon_tx), float(alt_tx))

            # Debugging info
            #self.logger.info("Received message from " + str(addr) + " : " + data + " at t=%.20f" % toa)

            # Forward received ADS-B message to all configured forwarders
            for f in self.forwarders:
                f.forward(message, toa)

    def stop(self):
        pass

if __name__ == '__main__':

    transponder = AdsbIn()
    transponder.start()
