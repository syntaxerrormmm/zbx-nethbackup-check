# Zabbix template to check for validity of backups on NethServer #

Included are the files to make agent checks using the Zabbix Agent on
NethServer machines.

Checks are performed twice a day (at 9.00 and at 14.00) and verifies that the
backup was successful and that the last backup was done during the last 7
days. The period of validity is customizable (changing the
`{$NETHBACKUP_VALIDITY}` macro inside host configuration inside Zabbix
frontend).

## Requisites ##

The template should work on Zabbix 3.x versions. To work, it requires:

* A working installation of NethServer 6.x or 7.x, Community or Enterprise;
* Zabbix Agent installed from [official Zabbix Repositories](http://repo.zabbix.com/). For instructions on installing Zabbix Agent on NethServer, please [see here](https://community.nethserver.org/t/howto-install-zabbix-3-4/7841/18);
* Python 2.x installed on NethServer.

## Installation ##

Clone the repository, then do the following inside your local working
directory as root user:

```
install -m 0755 -o root -g root nethbackup_check.py \
  /usr/local/bin/nethbackup_check.py
install -m 0644 -o root -g root userparameter_nethserver.conf \
  /etc/zabbix/zabbix_agent.d/userparameter_nethserver.conf
systemctl restart zabbix-agent
```

Then, import the `nethbackup_check.xml` template inside Zabbix frontend.
