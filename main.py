import logging

from connectors.binance_future import BinanceFutureClient
from interface.rootMain import Root

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_headler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_headler.setFormatter(formatter)
stream_headler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_headler)
logger.addHandler(file_handler)

# logger.debug("This message is important only when debugging the program")
# logger.info("This message just shows basic information")
# logger.warning("This message is about something you should pay attention to")
# logger.error("This message helps to debug an error that occurred in your program")


if __name__ == '__main__':
    binance = BinanceFutureClient('Apikey','SecretApiKey',False)
    root = Root(binance)
    root.mainloop()
