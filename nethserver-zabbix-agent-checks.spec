Summary: Adds some checks for monitoring NethServer backups via zabbix-agent
Name: nethserver-zabbix-agent-checks
Version: 1.0.1
Release: 1.ns7
License: GPLv3
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-root
Source0: %{name}-%{version}.tar.gz
Source1: LICENSE
URL: https://github.com/syntaxerrormmm/zbx-nethbackup-check
Group: Applications/Internet
Requires: zabbix-agent
Requires: python
Requires: sudo
Requires(post): systemd

%description
Adds some checks for monitoring NethServer backups via zabbix-agent

%install
install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_sysconfdir}/zabbix/zabbix_agentd.d
install -m0755 -o root -g root $RPM_SOURCE_DIR/nsmbcheck.py %{buildroot}/%{_bindir}/nsmbcheck.py
install -m0644 -o root -g root $RPM_SOURCE_DIR/userparameter_nethserver.conf %{buildroot}/%{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_nethserver.conf

%files
%{_bindir}/nsmbcheck.py
%{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_nethserver.conf
%license LICENSE

%post
/usr/bin/systemctl restart zabbix-agent

%postun
#if [ "$1" = 1 ]; then
#  #upgrade
#fi
if [ "$1" = 0 ]; then
    rm -f %{_bindir}/nsmbcheck.py
    rm -f %{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_nethserver.conf
    /usr/bin/systemctl restart zabbix-agent
fi

%changelog
* Wed Jan 04 2023 Emiliano Vavassori <syntaxerrormmm@gmail.com> - 1.0.1-1.ns7
- Bugfix: script returned syntax error while checking backups.

* Wed Apr 08 2020 Emiliano Vavassori <syntaxerrormmm@gmail.com> - 1.0.0-1.ns7
- First release for NethServer 7

