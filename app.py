from time import sleep

import sys
import signal
import logging

from src.path import Path
from src.subscribe.manag_sub_thread import ManagSubThread



def main_app():
    p = Path(['broker.json', 'schema.json'])
    p.search_paths()
    m = ManagSubThread(p)
    m.start()
    logging.basicConfig(filename="dmway.log", level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    logging.info("DMWAY service is started and ready to be used")
    while True:
        sleep(10)


if __name__ == '__main__':
    main_app()
