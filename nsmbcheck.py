#!/usr/bin/env python
# encoding: utf-8
# vim:sts=4:sw=4:tw=78

import datetime, re, sys, subprocess, glob
from time import strptime
from json import loads, dumps

# Multiple backup supported

class Backups:

    def __init__(self):
        """Reads e-smith 'backups' database to check for enabled backups."""

        self.__raw = loads(subprocess.check_output("/sbin/e-smith/db backups getjson", shell=True))
        self.backups = [ item['name'] for item in self.__raw if ('props' in
            item) and item['props']['status'] == 'enabled' ]
        self.backups.append('config')

    def discovery(self):
        """Returns enabled backups as output for the Zabbix discovery
        helper."""

        varname = '{#NSBACKUP}'

        backups = [ { varname: x } for x in self.backups ]
        return dumps({ 'data': backups })

class LogCheck:
    # Previously, the script checked for both the pre- and post- phases to be
    # included in the validity period and the status of the backup was good.

    def __init__(self, backupname="backup-data"):
        """Checks out metadata about each single multiple backup: checks the
        last log for the backup and extract the values required."""
        self.backupname = backupname
        self.status = 'FAILED'
        self.datetime = datetime.datetime.today()

        if self.backupname == 'config':
            # Backup name could be 'config'. In this case, we need to filter out
            # all the lines from /var/log/messages and consider the usual
            # conditions.

            # On newer NS versions (7.6), events are not pushed in
            # /var/log/messages anymore, so we rely on journalctl.

            # Generically filter out all lines not involved with backup-config
            logstream = subprocess.check_output("journalctl -t 'esmith::event'", shell=True).split('\n')
            contents = filter(lambda x: re.search(r"backup-config", x),
                    logstream)

            # From contents, I need to isolate two events: pre-backup-config
            # and post-backup-config.
            preline = filter(
                lambda x: re.search(r"Event pre-backup-config:", x),
            contents)[-1]

            postline = filter(
                lambda x: re.search(r"Event post-backup-config:", x),
            contents)[-1]

            lregex = r"^(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*Event p\w{2,3}-backup-config: (\w+)$"
            prem = re.match(lregex, preline)
            if prem:
                prestatus = prem.group(2)

            postm = re.match(lregex, postline)
            if postm:
                postdate = prem.group(1)
                poststatus = prem.group(2)

            strdatetime = postdate
            if prestatus == 'SUCCESS' and poststatus == 'SUCCESS':
                self.status = 'SUCCESS'

            # Fixing the date calculation
            self.datetime = datetime.datetime.strptime(postdate, '%b %d %H:%M:%S')
            self.datetime = self.datetime.replace(year=datetime.datetime.today().year)
            # If the date results in the future (which is not possible, since
            # we are seeing events in the past), remove 1 year.
            if self.datetime > datetime.datetime.today():
                self.datetime = self.datetime.replace(year=(datetime.datetime.today().year - 1))

        else:
            # Logs are in /var/log/backup dir, named after backup name.
            # Listing all logs in that folder, sorting them, then getting the
            # latest one.
            self.lastlogfile = sorted(glob.glob("/var/log/backup/backup-%s*.log" % str(self.backupname)), reverse=True)[0]

            f = open(self.lastlogfile, 'r')
            content = f.readlines()
            f.close()

            status = "FAILED"
            strdatetime = ""
            for line in content:
                s = re.match(r"^Backup status: (\w+)\n", line)
                if s:
                    status = s.group(1)

                d = re.match(r"^Backup ended at ([\d :-]+)\n", line)
                if d:
                    strdatetime = d.group(1)

            self.status = status

            # Fixing the date calculation
            self.datetime = datetime.datetime.strptime(postdate, '%b %d %H:%M:%S')
            self.datetime = self.datetime.replace(year=datetime.datetime.today().year)
            # If the date results in the future (which is not possible, since
            # we are seeing events in the past), remove 1 year.
            if self.datetime > datetime.datetime.today():
                self.datetime = self.datetime.replace(year=(datetime.datetime.today().year - 1))

    def verify(self, bakvalidity):
        """Verifies if the backup is valid: it is successful and it was done
        in the last {bakvalidity} days."""

        # Here we calculate the backup validity time
        end = datetime.datetime.combine(datetime.date.today(),
                datetime.datetime.max.time())
        start = end - datetime.timedelta(days = int(bakvalidity))
        start = datetime.datetime.combine(start, datetime.datetime.min.time())

        if self.status.lower() == 'success' and start <= self.datetime <= end:
            return 1

        return 0

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--discovery':
        print(Backups().discovery())
    elif len(sys.argv) == 3:
        a = LogCheck(sys.argv[1])
        print(a.verify(sys.argv[2]))
    else:
        print("""nsmbcheck.py - Verifies multiple NethServer backups.
--discovery - Create json data for low-level discovery for Zabbix.
<backupname> <backupduration> - Verifies if backup was fine and the last time
of execution is in the last <backupduration> days.""")
