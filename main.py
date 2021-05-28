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
    # binance = BinanceSpotClient('o2dBUFx9TsWoOhZMgOoQJHRHsdjsCrxs3QIODil1AgJXcE9gaeFs9cKMjaLpe4w0','cUH1YTs54uZ75tUMAr87KlFNPAsFlOHXAAqvwX9bCy61m8aHHkujd7gGvy6bosVH',False)
    # binance = BinanceSpotClient('2b1VMOH30KlPoM276FXLGYDgRW9nKoletj77i6Yh6EBHDnMMBr0BQ4jaEvc1dzEn','acemNJtGOcsqE44UsQaLOXcv7u3UCbhUFowlSCE1RRheUtw46OCUl67B9GF5EyKz',True)
    binance = BinanceFutureClient('42692c2916e81e669de7439f0a331dc71c580239e7dbc657a738dc5817a06e9a',
                                  '50c9e5028bf89cd159cda74adea64f36e997f15d88b35bc54b444944e97b9dd0', True)
    root = Root(binance)
    root.mainloop()
