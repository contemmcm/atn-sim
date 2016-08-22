import threading
import binascii
import MySQLdb
import os
import random
import time

from gps3 import gps3

from .adsb_feed import AdsbFeed

from atn import core_utils
from atn import emane_utils


class CoreFeed(AdsbFeed):

    gps_latitude = 0
    gps_longitude = 0
    gps_altitude = 0
    gps_track = 0
    gps_speed = 0
    gps_climb = 0
    gps_time = 0

    emane_latitude = 0
    emane_longitude = 0
    emane_altitude = 0
    emane_track = 0
    emane_speed = 0
    emane_climb = 0

    tracksrv_latitude = 0
    tracksrv_longitude = 0
    tracksrv_altitude = 0
    tracksrv_track = 0
    tracksrv_speed = 0
    tracksrv_climb = 0

    tracksrv_dbname = "atn_sim"
    tracksrv_dbuser = "atn_sim"
    tracksrv_dbpass = "atn_sim"
    tracksrv_dbhost = "172.17.255.254"

    nem_id = None
    node_name = None
    node_number = None
    session_id = None

    callsign = None
    icao24 = None

    def __init__(self):
        self.session_id = core_utils.get_session_id()
        self.node_name = core_utils.get_node_name()
        self.nem_id = core_utils.get_nem_id(node_name=self.node_name, session_id=self.session_id)
        self.node_number = core_utils.get_node_number(node_name=self.node_name, session_id=self.session_id)

    def get_position(self):
        # return self.gps_latitude, self.gps_longitude, self.gps_altitude
        return self.tracksrv_latitude, self.tracksrv_longitude, self.tracksrv_altitude

    def get_velocity(self):
        # return 45, 0, 100
        # azimuth, climb_rate, and speed
        return self.tracksrv_track, self.tracksrv_climb, self.tracksrv_speed

    def get_spi(self):
        return 0

    def get_ssr(self):
        return 0

    def get_callsign(self):
        if self.callsign is None:
            self.callsign = 'TAM%04d' % random.randint(0, 9999)
        return self.callsign

    def get_icao24(self):
        if self.icao24 is None:
            self.icao24 = binascii.b2a_hex(os.urandom(3))
        return self.icao24

    def get_capabilities(self):
        return 5

    def get_type(self):
        return 0

    def gps_start(self):
        t1 = threading.Thread(target=self.gps_read, args=())
        t1.start()

    def emane_start(self):
        t1 = threading.Thread(target=self.emane_read, args=())
        t1.start()

    def tracksrv_start(self):
        t1 = threading.Thread(target=self.tracksrv_read, args=())
        t1.start()

    def gps_read(self):
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()

        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)

                # Reading data from GPS stream
                lat = data_stream.TPV['lat']
                lon = data_stream.TPV['lon']
                alt = data_stream.TPV['alt']
                track = data_stream.TPV['track']
                speed = data_stream.TPV['speed']
                climb = data_stream.TPV['climb']
                time = data_stream.TPV['time']

                # Sanitizing location
                if lat == 'n/a' and lon == 'n/a' and alt == 'n/a':
                    self.gps_latitude = None
                    self.gps_longitude = None
                    self.gps_altitude = None
                else:
                    self.gps_latitude = lat
                    self.gps_longitude = lon
                    self.gps_altitude = alt

                # Sanitizing velocity
                if track == 'n/a' and speed == 'n/a' and climb == 'n/a':
                    self.gps_track = None
                    self.gps_speed = None
                    self.gps_climb = None
                else:
                    self.gps_track = track
                    self.gps_speed = speed
                    self.gps_climb = climb

                if time == 'n/a':
                    gps_time = None
                else:
                    gps_time = time

    def emane_read(self):

        while True:
            info = emane_utils.get_nem_location(self.nem_id)

            self.emane_latitude = info['latitude']
            self.emane_longitude = info['longitude']
            self.emane_altitude = info['altitude']
            self.emane_track = info['azimuth']
            self.emane_speed = info['magnitude']
            self.emane_climb = info['elevation']

            time.sleep(1)

    def tracksrv_read(self):

        db = MySQLdb.connect(self.tracksrv_dbhost, self.tracksrv_dbuser, self.tracksrv_dbpass, self.tracksrv_dbname)

        while True:
            cursor = db.cursor()
            query = "SELECT latitude, longitude, altitude, azimuth, magnitude, elevation FROM nem WHERE nem=%d" % self.nem_id
            cursor.execute(query)

            result = cursor.fetchone()

            lat = result[0]
            lon = result[1]
            alt = result[2]
            track = result[3]
            speed = result[4]
            climb = result[5]

            self.tracksrv_latitude = lat
            self.tracksrv_longitude = lon
            self.tracksrv_altitude = alt
            self.tracksrv_track = track
            self.tracksrv_speed = speed
            self.tracksrv_climb = climb

            cursor.close()

            time.sleep(0.5)
