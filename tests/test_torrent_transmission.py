
from pype.torrent import *
from mock import MagicMock

""" Tests for transmission torrent processors"""




""" Init with all configuration values needed"""
def init_ok_test():

    processor = TransmissionAddMagnetLinkProcessor({
                            TRANSMISSION_IP : "ip",
                            TRANSMISSION_PORT: "port",
                            TRANSMISSION_USER: "user",
                            TRANSMISSION_PASSWORD : "password"})


def init_fail_test():
    # TODO needs a better approach for exception detection in tests
    try:
        processor = TransmissionAddMagnetLinkProcessor({
                            TRANSMISSION_IP : "ip",
                            TRANSMISSION_PORT: "port",
                            TRANSMISSION_USER: "user"})

    except:
        pass

def add_all_test():
    # TODO
    pass

def add_all_failfirst_test():
    # TODO
    pass