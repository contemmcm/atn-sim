"""@package adsb_asterix_encode
"""

from aircraft_data import AircraftData
from . import asterix_utils

import threading
import socket
import binascii

__author__ = "Ivan Matias"
__date__ = "2016/04"


class AdsBAsterixEncode(object):
    """This class encodes ADS-B data in ASTERIX.

    This class is responsible for encode ADS-B data in ASTERIX CAT 21.

    """

    # BUFFER_SIZE [int]: Maximum size of the data buffer.
    BUFFER_SIZE = 1024

    def __init__(self):
        """The constructor.

        """
        # port [int]: Data receiving port.
        self.port = 0

        # net [string]: IPv4 address.
        self.net = '127.0.0.1'

    def create_socket(self, port):
        """Creates the socket for receiving the ADS-B messages.

        Args:
            port (int): Data receiving port.

        """
        # sock (socket):  The end point to send ASTERIX CAT 21.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = port

    def set_net(self, net):
        """Sets Ipv4 address.

        Args:
            net (string): IPv4 address

        """
        self.net = net

    def set_queue(self, queue):
        """Sets the queue for exchanging data between threads.

        Args:
            queue: The queue object.

        """
        # queue (Queue.Queue): The queue to exchange data.
        self.queue = queue

    def encode_data(self):
        """Receiving and encoding the ADS-B data in ASTERIX CAT 21.

        """
        while True:
            if not self.queue.empty():
                aircraft_table = self.queue.get()
                for k, v in aircraft_table.iteritems():
                    asterix_record = aircraft_table[k].to_asterix_record(k)
                    #print asterix_record
                    if asterix_record is not None:

                        # Encoding data to Asterix format
                        data_bin = asterix_utils.encode(asterix_record)

                        # print ("%x" % data_bin)
                        msg = hex(data_bin).rstrip("L").lstrip("0x")
                        self.sock.sendto(binascii.unhexlify(msg), (self.net, self.port))
                        print msg

    def start_thread(self):
        """Starts processing.

        """
        encode_thread = threading.Thread(target=self.encode_data, args=())
        encode_thread.start()

