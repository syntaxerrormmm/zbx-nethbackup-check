# Zabbix template to check for validity of backups on NethServer #

Included are the files to make agent checks using the Zabbix Agent on
[NethServer](https://www.nethserver.org) machines.

## Prerequisites ##

To use the provided template, you should already run a Zabbix Server version
3.0 or newer.

Checks provided will work on hosts with the following configuration:

* NethServer 7.x, Community or Enterprise;
* Zabbix Agent installed from [official Zabbix Repositories](http://repo.zabbix.com/). For instructions on installing Zabbix Agent on NethServer, please [see here](https://community.nethserver.org/t/howto-install-zabbix-3-4/7841/18);
* Python 2.x installed on the host;
* `sudo` on the host.

Be aware that the scripts are executed at *agent* level, thus they need to be
installed on *any* machines that need to be checked.

## Installation ##

### On the host to be monitored ###

I've created a small rpm package ready to be deployed, please check out the
[Releases](/syntaxerrormmm/zbx-nethbackup-check/releases) section. Deploy it like:

    yum -y install nethserver-zabbix-agent-checks-1.0.0-1.ns7.noarch.rpm

Please be aware that the script requires administrator permissions, so
it is indeed invoked via `sudo`. If you are using another user to run the
Agent (which you should do, anyways :) ) please adjust `sudo` like follows:

    echo "youruser ALL=(root) NOPASSWD: /usr/bin/nsmbcheck.py" >> /etc/sudoers.d/youruser
    chown 0440 /etc/sudoers.d/youruser
    visudo -c

### On the Zabbix Server ###

Just import the `NSMultiBackup_template.xml` file inside the
*Configuration > Templates > Import* function. Then assign the template
*Bak - Multiple NethServer Backups* to any host on which you have installed
the Zabbix Agent and the previous files.

## Configuration and internal working ##

Checks are performed twice a day (at 9.00 and at 14.00) and verifies that the
backup was successful and that the last backup was done during the last 7
days. The period of validity is customizable (changing the
`{$NSBAKVALIDITY}` macro inside host configuration inside Zabbix
frontend).

In the latest version, there's a `--discovery` options that, indeed, discovers
all the backups configured on the monitored host. The needed items and
triggers are then derived from the prototype ones inside the Template, based
on the discovery process.
