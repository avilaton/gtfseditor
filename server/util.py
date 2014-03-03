#!/usr/bin/python
# -*- coding: utf-8 -*-

import transitfeed
import datetime

# Time Utils         
def sec2hhmmss(sec):
    seconds = sec%60
    
    sec = sec-seconds
    min = int(sec/60)

    minutes = min%60    
    h = min-minutes
    hours = int(h/60)
    t = map(lambda d:"{0:02d}".format(d), [hours, minutes, seconds])
    formatedTime = ':'.join(t)

    return formatedTime

def hhmmss2sec(hhmmss):
    # hms = datetime.datetime.strptime(hhmmss,'%H:%M:%S')
    h,m,s = map(lambda x:int(x), hhmmss.split(':'))
    return h*60*60+m*60+s

def fixTimes(t0,t1):
    """ converts a time interval of the form 23:00:00, 01:30:00 into the 
    form 23:00:00, 25:30:00"""
    t_0 = datetime.datetime.strptime(t0,'%H:%M:%S')
    t_1 = datetime.datetime.strptime(t1,'%H:%M:%S')
    if (t_1-t_0).total_seconds() > 0:
        end_time = t_1.strftime('%H:%M:%S')
    elif (t_1-t_0).total_seconds() < 0:
        str(t_1.hour+24)
        end_time = str(t_1.hour+24) + t_1.strftime(':%M:%S')
    start_time = t_0.strftime('%H:%M:%S')
    return start_time,end_time

def main():
	print sec2hhmmss(69)
	print transitfeed.FormatSecondsSinceMidnight(69)

if __name__ == '__main__':
	main()