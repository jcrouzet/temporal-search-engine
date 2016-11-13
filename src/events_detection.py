import pandas as pd
import numpy as np
import statsmodels.api as sm

# Inspired from http://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data
def peaks_detection(y, lag=5, thresh=3.5, influence=0.5):

    assert len(y) > lag

    signal = np.zeros(len(y), int)

    filteredY = np.full(len(y), y, dtype=float)
    avgFilter = np.full(len(y), np.nan, dtype=float)
    stdFilter = np.full(len(y), np.nan, dtype=float)
    avgFilter[lag-1] = np.mean(y[0:(lag-1)])
    stdFilter[lag-1] = np.std(y[0:(lag-1)])

    for i in range(lag, len(y)):
        if np.abs(y[i] - avgFilter[i-1]) > thresh*stdFilter[i-1]:
            if y[i] > avgFilter[i-1]:
                signal[i] += 1
            else:
                signal[i] -= 1

            filteredY[i] = influence*y[i] + (1-influence)*filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i])

        else:
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i])

    return((signal, avgFilter, stdFilter))


def events_list(signal, hist, size=20):

    events = list()
    amplitude = list()
    i = 0

    while i < len(signal):
        if signal[i] == 1:
            start = i
            end = i
            tmp = hist[start-1]
            while end < len(signal):
                if signal[end] == signal[start]:
                    end += 1
                    tmp += hist[end-1]
                else:
                    break

            events.append((start, end))
            amplitude.append(tmp)
            i = end + 1
        else:
            i += 1

    return([x for (y, x) in sorted(zip(amplitude, events), reverse=True)][:(min(len(events), size))])
