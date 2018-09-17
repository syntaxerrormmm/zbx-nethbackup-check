#!/usr/bin/env python
# vim:sts=4:sw=4:tw=78
# encoding: utf-8

import datetime, re, sys
import subprocess

# As of 11/09/2018, format of backup log files changed a bit.
# To be more compliant and forward compatible, events will be checked against
# system log.
LOGFILE = "/var/log/messages"

class LogCheck:

    def __init__(self):
        """Extracts information for the backups from the system messages."""

        # Initializing default response.
        self.config = {
                'pre': {
                    'date': datetime.datetime.min,
                    'status': False
                },
                'post': {
                    'date': datetime.datetime.min,
                    'status': False
                }
        }
        self.data = {
                'pre': {
                    'date': datetime.datetime.min,
                    'status': False
                },
                'post': {
                    'date': datetime.datetime.min,
                    'status': False
                }
        }
        
        # I open up the logfile and scan for lines which matches the backup
        # phases (pre/post).
        log_arr = filter(lambda x: re.search(r'Event: p(re|ost)-backup', x),
                open(LOGFILE, 'r').readlines())

        # Once extracted the needed lines, I will extract date and status both
        # for pre and post backup for configuration
        # CAUTION: the space after the event is intended, as to filter out the
        # only lines with the result of the task
        bakcfg_log = filter(lambda x: re.search(r'backup-config ', x),
                log_arr)

        # Now, I filter by event: pre or post.
        # Let's start with pre.
        prebakcfg_log = filter(lambda x: re.search(r'pre-backup', x),
                bakcfg_log)

        if len(prebakcfg_log) > 0:
            # If no lines are filtered with previous filters, it may be
            # because there are no tasks 
            # Getting last line for pre-backup-config
            prebakcfg_line = prebakcfg_log[-1].strip()

            # Now parsing the line, reconstructing date/time and status
            month, day, time, name, event, event_str, event_name, status = re.split(r" *", prebakcfg_line)

            # Small correction for the day, which is not zero-padded
            if int(day) <= 9:
                day = '0' + day

            year = str(datetime.datetime.now().year)

            self.config['pre'] = {
                    'date': datetime.datetime.strptime("%s %s %s %s" % (day,
                        month, year, time), "%d %b %Y %X"),
                    'status': True if re.search(r'SUCCESS', status) else False
            }
        
        # Then with post
        postbakcfg_log = filter(lambda x: re.search(r'post-backup', x),
                bakcfg_log)


        if len(postbakcfg_log) > 0:
            # Getting last line for post-backup-config
            postbakcfg_line = postbakcfg_log[-1].strip()

            # Now parsing the line, reconstructing date/time and status
            month, day, time, name, event, event_str, event_name, status = re.split(r" *", postbakcfg_line)

            # Small correction for the day, which is not zero-padded
            if int(day) <= 9:
                day = '0' + day

            self.config['post'] = {
                    'date': datetime.datetime.strptime("%s %s %s %s" % (day,
                        month, year, time), "%d %b %Y %X"),
                    'status': True if re.search(r'SUCCESS', status) else False
            }

        # Now, for the data backups
        # CAUTION: the space after the event is intended, as to filter out the
        # only lines with the result of the task
        bakdata_log = filter(lambda x: re.search(r'backup-data ', x),
                log_arr)

        # Now, I filter by event: pre or post.
        # Let's start with pre.
        prebakdata_log = filter(lambda x: re.search(r'pre-backup', x),
                bakdata_log)

        if len(prebakdata_log) > 0:
            # Getting last line for pre-backup-data
            prebakdata_line = prebakdata_log[-1].strip()

            # Now parsing the line, reconstructing date/time and status
            month, day, time, name, event, event_str, event_name, status = re.split(r" *", prebakdata_line)

            # Small correction for the day, which is not zero-padded
            if int(day) <= 9:
                day = '0' + day

            self.data['pre'] = {
                    'date': datetime.datetime.strptime("%s %s %s %s" % (day,
                        month, year, time), "%d %b %Y %X"),
                    'status': True if re.search(r'SUCCESS', status) else False
            }
        
        # Then with post
        postbakdata_log = filter(lambda x: re.search(r'post-backup', x),
                bakdata_log)

        if len(postbakdata_log) > 0:
            # Getting last line for post-backup-config
            postbakdata_line = postbakdata_log[-1].strip()

            # Now parsing the line, reconstructing date/time and status
            month, day, time, name, event, event_str, event_name, status = re.split(r" *", postbakdata_line)

            # Small correction for the day, which is not zero-padded
            if int(day) <= 9:
                day = '0' + day

            self.data['post'] = {
                    'date': datetime.datetime.strptime("%s %s %s %s" % ( day,
                        month, year, time), "%d %b %Y %X"), 
                    'status': True if re.search(r'SUCCESS', status) else False
            }

    def verify(self, baktype, bakvalidity):
        """Verifies the backup type both for success/failure and validity (last
        backup done in a specified period of times)."""
    
        # Here we calculate the backup validity time
        end = datetime.datetime.combine(datetime.date.today(),
                datetime.datetime.max.time())
        start = end - datetime.timedelta(days = int(bakvalidity))
        start = datetime.datetime.combine(start, datetime.datetime.min.time())

        if baktype.lower() == 'config':
            if self.config['pre']['status'] and self.config['post']['status'] and start <= self.config['pre']['date'] <= end and start <= self.config['post']['date'] <= end:
                return 1
    
            return 0
    
        else:
            # Should be 'data' type
            if self.data['pre']['status'] and self.data['post']['status'] and start <= self.data['pre']['date'] <= end and start <= self.data['post']['date'] <= end:
                return 1
    
            return 0

if __name__ == '__main__':
    a = LogCheck()
    print(a.verify(sys.argv[1], sys.argv[2]))
