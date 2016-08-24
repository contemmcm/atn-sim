import ConfigParser
import logging
import MySQLdb
import netifaces as ni
import os
import threading
import time

import core_utils
import emane_utils

from .network import mcast_socket

from emanesh.events import EventService
from emanesh.events import LocationEvent


class TrackServer:

    update_interval = 1.0

    log_file = "track_server.log"
    log_level = logging.DEBUG

    net_tracks = "235.12.2.4"
    net_iface = "ctrl0"

    db_name = 'atn_sim'
    db_user = 'atn_sim'
    db_pass = 'atn_sim'
    db_host = '172.17.255.254'

    def __init__(self, config="track_server.cfg"):

        self.db = MySQLdb.connect(self.db_host, self.db_user, self.db_pass, self.db_name)

        # Logging
        logging.basicConfig(filename=self.log_file, level=self.log_level, filemode='w',
                            format='%(asctime)s %(levelname)s: %(message)s')

        self.config = None

        if os.path.exists(config):
            self.config = ConfigParser.ConfigParser()
            self.config.read(config)


            # self.id = conf.get("General", "id")

    def start(self):
        logging.info("Initiating sever")

        self._init_nodes_table()
        self._init_nems_table()
        self._init_mapings()

        t1 = threading.Thread(target=self._update, args=())
        t2 = threading.Thread(target=self.listen, args=())

        t1.start()
        t2.start()

    def stop(self):
        pass

    def listen(self):
        FT_TO_M = 0.3048
        KT_TO_MPS = 0.51444444444

        service = EventService(('224.1.2.8', 45703, self.net_iface))

        # This method is very slow. Future versions will implement distributed version of it.
        self.nodes = []

        # Retrieving list of nodes
        nodes = emane_utils.get_all_locations()

        for n in nodes:
            self.nodes.append(n["nem"])

        # IP address of incoming messages
        ip = ni.ifaddresses(self.net_iface)[2][0]['addr']

        print "Control IP:   %s" % ip
        print "Listen Addr.: %s:" % self.net_tracks

        sock = mcast_socket.McastSocket(local_port=1970, reuse=True)
        sock.mcast_add(self.net_tracks, ip)  # Endereco de pistas

        while True:

            event = LocationEvent()

            data, sender_addr = sock.recvfrom(1024)

            message = data.split("#")

            # ex: 101#114#1#7003#-1#4656.1#-16.48614#-47.947058#210.8#9.7#353.9#TAM6543#B737#21653.3006492
            msg_ver = int(message[0])
            msg_typ = int(message[1])

            if msg_typ == 114:  # 114: message coming from newton.py
                msg_num = int(message[2])  # node id
                msg_ssr = message[3]
                msg_spi = int(message[4])  # if spi > 0, SPI=ON, otherwise SPI=OFF
                msg_alt = float(message[5])  # altitude (feet)
                msg_lat = float(message[6])  # latitude (degrees)
                msg_lon = float(message[7])  # longitude (degrees)
                msg_vel = float(message[8])  # velocity (knots)
                msg_cbr = float(message[9])  # climb rate (m/s)
                msg_azm = float(message[10])  # azimuth (degrees)
                msg_csg = message[11]  # callsign
                msg_per = message[12]  # aircraft performance type
                msg_tim = float(message[13])  # timestamp (see "hora de inicio")

                if msg_num in self.nodes:
                    if msg_num in self.track2nem:
                        nemid = self.track2nem[msg_num]
                    else:
                        nemid = msg_num

                    print (msg_num, nemid)

                    #
                    # Update node's position using Emane API
                    #
                    event.append(nemid, latitude=msg_lat, longitude=msg_lon, altitude=msg_alt * FT_TO_M,
                                 azimuth=msg_azm, magnitude=msg_vel * KT_TO_MPS, elevation=0.0)

                    #
                    # Update transponder's parameters using database shared memory
                    #
                    cursor = self.db.cursor()
                    cursor.execute("SELECT callsign, performance_type FROM transponder WHERE nem_id=%d" % nemid)
                    result = cursor.fetchone()

                    db_callsign = result[0]
                    db_perftype = result[1]

                    if db_callsign[0] != msg_csg or db_perftype != msg_per:
                        sql = "UPDATE transponder SET callsign='%s', performance_type='%s' WHERE nem_id=%d" % (msg_csg,
                                                                                                               msg_per,
                                                                                                               nemid)
                        cursor.execute(sql)
                        self.db.commit()
                    cursor.close()

            service.publish(0, event)

    def _update(self):
        while True:
            t0 = time.time()
            nodes = emane_utils.get_all_locations()

            for n in nodes:
                cursor = self.db.cursor()
                sql = "UPDATE nem set latitude=%f, longitude=%f, altitude=%f, " \
                      "pitch=%f, roll=%f, yaw=%f, " \
                      "azimuth=%f, elevation=%f, magnitude=%f,  " \
                      "last_update=now() WHERE id=%d" % (n['latitude'], n['longitude'], n['altitude'],
                                        n['pitch'], n['roll'], n['yaw'],
                                        n['azimuth'], n['elevation'], n['magnitude'],
                                        n['nem'])
                cursor.execute(sql)

                self.db.commit()
                cursor.close()

            dt = time.time() - t0

            # Logging
            logging.info("Tables updated successfully. Processing time: %f s" % dt)
            if dt > self.update_interval:
                logging.warning("Position updates is taking longer than %f s" % self.update_interval)

            dt = time.time() - t0

            time.sleep(self.update_interval - dt)

    def _init_nodes_table(self):

        logging.info("Initiating table NODE")

        session = int(core_utils.get_session_id())
        node_number, node_name = core_utils.get_node_list()

        cursor = self.db.cursor()

        # Clean table
        cursor.execute("DELETE FROM node")

        for n in range(0, len(node_number)):
            sql = "INSERT INTO node (id, name, session) VALUES (%d, '%s', %d)" % (node_number[n], node_name[n], session)
            cursor.execute(sql)

        self.db.commit()

        cursor.close()

    def _init_nems_table(self):

        logging.info("Initiating table NEM")

        node_names, node_devs, nemids = core_utils.get_nem_list()

        cursor = self.db.cursor()

        sql = "DELETE FROM nem"
        cursor.execute(sql)
        logging.debug(sql)

        for n in range(0, len(node_names)):
            sql = "INSERT INTO nem (id, node_id, iface) VALUES (%d, (SELECT id FROM node WHERE name='%s'), '%s' )" % (nemids[n], node_names[n], node_devs[n])
            cursor.execute(sql)
            logging.debug(sql)

        self.db.commit()
        cursor.close()

    def _init_mapings(self):

        self.track2nem = {}

        if self.config is None:
            return

        data = self.config.items("Tracks")

        for i in range(0, len(data)):
            nodename = data[i][0]
            tracknumber = data[i][1]

            # node number
            sql = "SELECT a.id, b.id FROM node a, nem b WHERE a.name='%s' and a.id=b.node_id" % nodename
            cursor = self.db.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            nodenumber = result[0]
            nemid = result[1]

            self.track2nem[tracknumber] = nemid


if __name__ == '__main__':
    t = TrackServer()
    t.start()
