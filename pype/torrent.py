import logging
import sys

from core import *
from pype.model import BaseItem

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
class TransmissionAddTorrentProcessor(AbstractListProcessor):

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
            torrent_add_result = self.__tclient.add_torrent(item.getValue())
            logger.info("Result : " + str(torrent_add_result))
            return  [item]
        except:
            logger.warn("Error adding torrent"+str(sys.exc_info()[0]))



    def __initTransmissionClient(self):

        try:
            # Obtain transmission client
            self.__tclient = transmissionrpc.Client(self.__config[TRANSMISSION_IP],
                                                    port=self.__config[TRANSMISSION_PORT],
                                                    user=self.__config[TRANSMISSION_USER],
                                                    password=self.__config[TRANSMISSION_PASSWORD])
            logger.debug("Transmission client created")
            ## TODO Add configuration (no password!) to log
        except ValueError:
            logger.error("Errors creating transmission client"+ str(sys.exc_info()[0]))


    def __checkConfiguration(self,config):
        ## TODO Must be implemented (Issue #4)
        return (not config is None) and (TRANSMISSION_IP in config) and (TRANSMISSION_PORT in config) and (TRANSMISSION_USER in config) and (TRANSMISSION_PASSWORD in config)




class TransmissionClientConfig():
    """ Item value for TransmissionChangeStatusProcessor"""
    def __init__(self,host,port,user,password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password



TRANSMISSION_CLIENT_CONFIG = "transmission_client_config"
TRANSMISSION_TORRENT_CURRENT_STATUS = "transmission_torrent_current_status"
# Valid status
# stopped, downloading
TRANSMISSION_TORRENT_OPERATION = "transmission_torrent_operation"
TRANSMISSION_TORRENT_OPERATION_START = "transmission_torrent_operation_start"
TRANSMISSION_TORRENT_OPERATION_STOP = "transmission_torrent_operation_stop"

class TransmissionChangeStatusProcessor(AbstractListProcessor):

    __config = None

    def __init__(self,config):

        if self.validateConfig(config):
            self.__config = config


    def process(self,item):

        result = []
        logger.debug(" Item value type : " + str(type(item.getValue())))
        if type(item.getValue())==type(TransmissionClientConfig(None,None,None,None)):
            clientConfig = item.getValue()
            tclient = transmissionrpc.Client(clientConfig.host,clientConfig.port,clientConfig.user,clientConfig.password)

            torrents = tclient.get_torrents()
            for t in torrents:
                self.__changeTorrentStatus(tclient,t)
                result.append(BaseItem({"torrent-transmission":True},t))

        else:
            logger.warning("Unknown item value type " + str(type(item.getValue())))

        return result
    def validateConfig(self, config):
        return True


    def __changeTorrentStatus(self,tclient,torrent):
        """ Change torrent status as states configuration """
        logger.debug("Torrent " + str(torrent.status) + " - " +str(torrent.name))
        if torrent.status == self.__config[TRANSMISSION_TORRENT_CURRENT_STATUS]:
            logger.info("Torrent " + str(torrent.id) + " is in status " + str(torrent.status))

            # Do operation
            operation = self.__config[TRANSMISSION_TORRENT_OPERATION]
            if  operation == TRANSMISSION_TORRENT_OPERATION_START:
                logger.info("Starting torrent " + str(torrent.name))
                tclient.start_torrent(torrent.id,bypass_queue='true')
            elif operation == TRANSMISSION_TORRENT_OPERATION_STOP:
                logger.info("Stopping torrent " + str(torrent.name))
                tclient.stop_torrent(torrent.id)
            else:
                logger.warning("Unknown operation" + str(operation))
        pass
