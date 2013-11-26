
from pype.torrent import *
from mock import MagicMock
from mock import patch
""" Tests for transmission torrent processors"""

# Configuration test values
TEST_IP = "ip"
TEST_PORT = "port"
TEST_USER = "user"
TEST_PASSWORD = "password"
""" Init with all configuration values needed"""
def init_ok_test():

    processor = __getConfiguredProcessor()

def init_fail_test():
    # TODO needs a better approach for exception detection in tests
    try:
        processor = TransmissionAddTorrentProcessor({
                            TRANSMISSION_IP : TEST_IP,
                            TRANSMISSION_PORT: TEST_PORT,
                            TRANSMISSION_USER: TEST_USER})

    except:
        pass



# client needed for below tests
@patch('pype.model.BaseItem')
@patch('pype.model.BaseItem')
@patch('transmissionrpc.Client')
def add_all_test(client,item1,item2):
    # TODO
    list = [item1,item2]

    processor = __getConfiguredProcessor()
    result = processor.processList(list)

    assert client.called
    #TODO assert result size must be 2
    #TODO assert client called twice

def add_all_failfirst_test():
    # TODO
    pass


def __getConfiguredProcessor():

    return TransmissionAddTorrentProcessor({
                            TRANSMISSION_IP : TEST_IP,
                            TRANSMISSION_PORT: TEST_PORT,
                            TRANSMISSION_USER: TEST_USER,
                            TRANSMISSION_PASSWORD : TEST_PASSWORD})
