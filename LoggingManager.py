import logging as log
from datetime import datetime

import BackendCore


def startLoggingLoop():
    log.basicConfig(level=log.INFO, filename="NetCap_Capture_Log.log", filemode="w", format="")
    log.info(datetime.now())
    data = []
    network_data = BackendCore.get_network_connections()
    for string in network_data:
        log.info("")
        log.info("CONNECTION: "+str(string))
def startLogging():
    log.basicConfig(level=log.INFO, filename="NetCap_Capture_Log.log", filemode="w", format="")
    log.info("NetCap v 0.1 logging started")
def logWarning(data):
    log.basicConfig(level=log.INFO, filename="NetCap_Log.log", filemode="w", format="")
    log.info("warning: "+str(data))
