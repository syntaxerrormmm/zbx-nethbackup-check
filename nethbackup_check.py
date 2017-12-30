#!/usr/bin/env python
# vim:sts=4:sw=4
# encoding: utf-8

import datetime, re, sys

BACKUPTYPE = { 
    'Data':	'/var/log/backup-data.log',
    'Config':	'/var/log/backup-config.log'
}

def backup_check(backuptype, validity):
    f = open(BACKUPTYPE[backuptype])
    lastline = f.readlines()[-1]
    f.close()
    # Splitting last line once read
    lastline_arr = str.split(lastline)

    # From last line I will also extract the date
    check = datetime.datetime.strptime(lastline_arr[0], '%Y-%m-%d').date()
    end = datetime.date.today()
    start = end - datetime.timedelta(days = int(validity))

    # Verifies the status of the last backup
    if start <= check <= end and re.match(r'SUCCESS', lastline_arr[3]):
	return 1

    return 0

if __name__ == '__main__':
    print(backup_check(sys.argv[1], sys.argv[2]))
