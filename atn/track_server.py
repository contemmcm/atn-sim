import logging
import MySQLdb
import threading
import time

import core_utils
import emane_utils


class TrackServer:

    update_interval = 1.0

    log_file = "track_server.log"
    log_level = logging.DEBUG

    db_name = 'atn_sim'
    db_user = 'atn_sim'
    db_pass = 'atn_sim'
    db_host = '172.17.255.254'

    def __init__(self):

        self.db = MySQLdb.connect(self.db_host, self.db_user, self.db_pass, self.db_name)

        # Logging
        logging.basicConfig(filename=self.log_file, level=self.log_level, filemode='w',
                            format='%(asctime)s %(levelname)s: %(message)s')

    def start(self):
        logging.info("Intiating sever")

        self._init_nodes_table()
        self._init_nems_table()

        t1 = threading.Thread(target=self._update, args=())
        t1.start()

    def stop(self):
        pass

    def _update(self):
        while True:
            t0 = time.time()
            nodes = emane_utils.get_all_locations()

            cursor = self.db.cursor()
            for n in nodes:
                sql = "UPDATE nem set latitude=%f, longitude=%f, altitude=%f, " \
                      "pitch=%f, roll=%f, yaw=%f, " \
                      "azimuth=%f, elevation=%f, magnitude=%f,  " \
                      "last_update=now() WHERE nem=%d" % (n['latitude'], n['longitude'], n['altitude'],
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
            sql = "INSERT INTO nem (nem, node_id, iface) VALUES (%d, (SELECT id FROM node WHERE name='%s'), '%s' )" % (nemids[n], node_names[n], node_devs[n])
            cursor.execute(sql)
            logging.debug(sql)

        self.db.commit()
        cursor.close()

if __name__ == '__main__':
    t = TrackServer()
    t.start()
