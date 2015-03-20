Summary:	proxy ARP daemon
Name:		choparp
Version:	0
#Rel:       YYMM.#
Release:    1503.1
%define _gitver   51c1f0de12585ee2e8c251d44e953f6f4de3ba70
License:	BSD
Group:		Applications/Networking
Source0:    https://github.com/quinot/choparp/archive/%{_gitver}.zip
# Source0-md5:	73386c6302f74124d9987b77fef3927a
Source3:    sample.conf
Source4:    choparp.sysconfig
Source5:    choparp-service-generator
Source6:    choparp.target
Source7:    choparp@.service
URL:		https://github.com/quinot/choparp
BuildRequires:	libpcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
choparp is a proxy ARP daemon. It listens for ARP requests on a
network interface, and sends ARP replies with a specified MAC
addresses when the requested IP addresses matches a user-provided
list.

%prep
%setup -q -n %{name}-%{_gitver}

%build
cd src
gcc -o choparp choparp.c -lpcap

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8/} \
           $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
           $RPM_BUILD_ROOT/etc/{sysconfig,%{name}} \
           $RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}} \
           $RPM_BUILD_ROOT/lib/systemd/system-generators

install src/choparp $RPM_BUILD_ROOT%{_sbindir}

install src/choparp.8 $RPM_BUILD_ROOT%{_mandir}/man8/

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/eth0.conf
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -p %{SOURCE5} $RPM_BUILD_ROOT/lib/systemd/system-generators/%{name}-service-generator
install -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.target
install -p %{SOURCE7} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}@.service


%clean
rm -rf $RPM_BUILD_ROOT

%post
%service %{name} restart
%systemd_post %{name}.target

%preun
if [ "$1" = "0" ]; then
    %service %{name} stop
fi
%systemd_preun %{name}.target

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) /lib/systemd/system-generators/%{name}-service-generator
%{systemdunitdir}/%{name}.target
%{systemdunitdir}/%{name}@.service
%attr(770,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/eth0.conf
%{_mandir}/man8/*

