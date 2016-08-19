from gps3 import gps3

from .adsb_feed import AdsbFeed


class CoreemuFeed(AdsbFeed):

    latitude = 0
    longitude = 0
    altitude = 0

    nemid = None
    nodename = None
    nodenumber = None
    sessionid = None

    def __init__(self):
        pass

    def get_position(self):
        return self.latitude, self.longitude, self.altitude

    def get_velocity(self):
        return 0, 0, 0

    def get_spi(self):
        return 0

    def get_callsign(self):
        return None

    def get_icao24(self):
        raise None

    def start_gps(self):
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

                # Sanitizing
                if lat == 'n/a' and lon == 'n/a' and alt == 'n/a':
                    self.latitude = None
                    self.longitude = None
                    self.altitude = None
                else:
                    self.latitude = lat
                    self.longitude = lon
                    self.altitude = alt
