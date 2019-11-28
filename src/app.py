from time import sleep, time


import sys
import signal
import logging

from src.subscribe.manag_sub_thread import ManagSubThread

sub = None


def running_handler(signum, frame):
    global sub
    try:
        print("Cleaning process")
        sub.stop_running()
        sub.join()
    except:
        pass
    sys.exit(0)


def main_app():
    global sub
    signal.signal(signal.SIGINT, running_handler)
    m = ManagSubThread()
    m.start()
    logging.basicConfig(filename="dmway.log", level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info("DMWAY service is started and ready to be used")
    while True:
        sleep(10)


if __name__ == '__main__':
    main_app()
