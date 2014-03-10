from pype.torrent import TransmissionClientConfig, \
    TransmissionChangeStatusProcessor, \
    TRANSMISSION_TORRENT_OPERATION, \
    TRANSMISSION_TORRENT_CURRENT_STATUS, TRANSMISSION_TORRENT_OPERATION_START
from pype.model import BaseItem

# logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Transmission torrent change status sample
# Starts all stopped torrents

transmission_config = TransmissionClientConfig("host", "port", "user", "password")

processor = TransmissionChangeStatusProcessor({TRANSMISSION_TORRENT_CURRENT_STATUS:'stopped',
                                               TRANSMISSION_TORRENT_OPERATION:TRANSMISSION_TORRENT_OPERATION_START})

item = BaseItem(None, transmission_config)

result = processor.process(item)


