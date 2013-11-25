import logging
import sys

from core import *

logger = logging.getLogger("pype.torrent")

""" Processor for torrents downloading"""

""" Transmission integration """
import transmissionrpc


## Transmission client config constants

TRANSMISSION_IP = "transmissionip"
TRANSMISSION_PORT = "transmissionport"
TRANSMISSION_USER = "transmissionuser"
TRANSMISSION_PASSWORD = "transmissionpassword"



""" Transmission Add Magnet Link Processor

 @see https://trac.transmissionbt.com/wiki/EditConfigFiles#RPC
 @see white list in previous link for connectivity issues

"""
class TransmissionAddMagnetLinkProcessor(AbstractListProcessor):

    __config = {}

    #Transmission client
    __tclient = None

    def __init__(self,config):

        self.__config = config

        if not self.__checkConfiguration(config):
            raise "Wrong configuration provided " + str(config)


    def process(self,item):
        if self.__tclient is None:
            self.__initTransmissionClient()

        try:
            logger.info("Adding torrent "+str(item.getValue()))
            self.__tclient.add_torrent(item.getValue())
        except:
            logger.warn("Error adding torrent"+sys.exc_info()[0])



    def __initTransmissionClient(self):

        try:
            # Obtain transmission client
            self.__tclient = transmissionrpc.Client(self.__config[TRANSMISSION_IP],
                                                    port=self.config[TRANSMISSION_PORT],
                                                    user=self.__config[TRANSMISSION_USER],
                                                    password=self.__config[TRANSMISSION_PASSWORD])
            logger.debug("Transmission client created")
            ## TODO Add configuration (no password!) to log
        except ValueError:
            logger.error("Errors creating transmission client"+ str(sys.exc_info()[0]))


    def __checkConfiguration(self,config):
        ## TODO Must be implemented (Issue #4)
        return true
