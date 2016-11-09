import sys
import getopt

import numpy as np

from query import *
from events_detection import *
from timeline_json import *

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 2:
        print >>sys.stderr, "usage: " + argv[0] + " <query>"
        return 2

    hist, dates = query_hist(argv[1])

    # Peak detection
    lag = 60
    thresh = 3.5
    influence = 0.01

    sig, avg, std = peaks_detection(hist, lag, thresh, influence)

    # Events
    events = events_list(sig)
    
    # Timeline creation
    timeline_json(events, dates, argv[1])

if __name__ == "__main__":
    sys.exit(main())
