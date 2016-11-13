import sys
import subprocess
import argparse

import numpy as np

from query import *
from events_detection import *
from basic_detection import *
from timeline_json import *
from html_creation import *


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("query",
                    help="This is your query. This is a needed argument")
    parser.add_argument("-b", "--begin",
                    help="Timerange start with format yyyy-MM-dd")
    parser.add_argument("-e", "--end",
                    help="Timerange end with format yyyy-MM-dd")
    parser.add_argument("-p", "--basicpeak", action="store_true",
                    help="Use basic peak detection")
    parser.add_argument("-s", "--size", type=int,
                    help="Configure number of results")
    args = parser.parse_args()

    begin = "2012-04-01"
    end = "2015-08-31"
    size = 20
    basic = 1

    quer = args.query

    if args.begin:
        begin = args.begin

    if args.end:
        end = args.end

    if args.basicpeak:
        basic = 0

    if args.size:
        size = args.size

    # If quer is "", raises error (this case might has been raised earlier)
    if quer=="":
        usage()
        sys.exit()

    # Query Elasticsearch
    hist, dates = query_hist(quer,begin,end)

    len_hist = len(hist)

    # Case with no result to the query
    if len_hist == 0:
        print("Pas de résultat :(")
        return 2

    # Case with very short range of result : using unique range for results
    if len_hist <= 10:
        events = [(1,len_hist)]
    else:
        # When less than 60 counts, using basic pics detection
        if len_hist <= 60:
            basic = 0

        # Basic peak detection
        if basic==0 :
            events = peekadpt(hist)

        # Peak detection
        else:
            lag = 60
            thresh = 3.5
            influence = 0.01
            sig, avg, std = peaks_detection(hist, lag, thresh, influence)
            events = events_list(sig, hist, size)

    # Timeline creation
    res_json = timeline_json(events, dates, quer)

    # HTML creation
    html_creation(res_json)

    # Launch of result web page
    subprocess.run(["firefox", "results/temporal_search_results.html"])

if __name__ == "__main__":
    main(sys.argv[1:])

#if __name__ == "__main__":
#    sys.exit(main())
