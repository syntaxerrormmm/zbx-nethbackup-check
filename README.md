# Zabbix template to check for validity of backups on NethServer #

Included are the files to make agent checks using the Zabbix Agent on
[NethServer](https://www.nethserver.org) machines.

Checks are performed twice a day (at 9.00 and at 14.00) and verifies that the
backup was successful and that the last backup was done during the last 7
days. The period of validity is customizable (changing the
`{$NETHBACKUP_VALIDITY}` macro inside host configuration inside Zabbix
frontend).

## Requisites ##

To use the provided template, you should already run a Zabbix Server version
3.0 or newer.

Checks provided will work on hosts with the following configuration:

* NethServer 6.x or 7.x, Community or Enterprise;
* Zabbix Agent installed from [official Zabbix Repositories](http://repo.zabbix.com/). For instructions on installing Zabbix Agent on NethServer, please [see here](https://community.nethserver.org/t/howto-install-zabbix-3-4/7841/18);
* Python 2.x installed on the host.

## Checks installation ##

On a host to monitor with root user, clone the repository, then do the
following inside your local working directory:
```
install -m 0755 -o root -g root nethbackup_check.py \
  /usr/local/bin/nethbackup_check.py
install -m 0644 -o root -g root userparameter_nethserver.conf \
  /etc/zabbix/zabbix_agent.d/userparameter_nethserver.conf
systemctl restart zabbix-agent
```

On the Zabbix Server, import the `nethbackup_check.xml` file inside the
*Configuration > Templates > Import* function. Then assign the template
*NethServer backup check* to any host on which you have installed the Zabbix
Agent and the previous files.
