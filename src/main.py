import sys
import getopt

import numpy as np

from query import *
from events_detection import *
from basic_detection import *
from timeline_json import *
from html_creation import *


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) == 2:
        begin = "2012-04-01"
        end = "2015-08-31"
        basic=1
    elif len(argv) == 3 and argv[2]=="basic":
        begin = "2012-04-01"
        end = "2015-08-31"
        basic=0
    elif len(argv) == 5 and argv[4]=="basic":
        basic=0
    elif len(argv) != 4:
        print("Usage: " + argv[0] + " <query> [<date_debut> <date_fin>] [basic]", file=sys.stderr)
        return 2
    else:
        begin = argv[2]
        end = argv[3]
        basic = 1

    hist, dates = query_hist(argv[1],begin,end)

    len_hist = len(hist)

    if len_hist == 0:
      print("Pas de résultat :(")
      return 2

    if len_hist <= 10:
        events = [(1,len_hist)]
    else:
        # When less than 60 counts, using basic pics detection
        if len_hist <= 60:
            basic = 0

        # Peak detection
        if basic==0 :
            events = peekadpt(hist)
        else:
            lag = 60
            thresh = 3.5
            influence = 0.01
            sig, avg, std = peaks_detection(hist, lag, thresh, influence)
            events = events_list(sig)

    # Timeline creation
    res_json = timeline_json(events, dates, argv[1])

    # HTML creation
    html_creation(res_json)

if __name__ == "__main__":
    sys.exit(main())
