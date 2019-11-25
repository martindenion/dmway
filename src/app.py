from time import sleep, time

from src.format.format import Verification
from src.publish.manage_pub_thread import ManagPubThread
from src.publish.publish import PubThread
from src.subscribe.manag_sub_thread import ManagSubThread
from src.subscribe.subscribe import SubThread
import sys
import signal

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
    m.join()



if __name__ == '__main__':
    main_app()