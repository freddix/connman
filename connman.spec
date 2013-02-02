Summary:	Connection Manager
Name:		connman
Version:	1.11
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.kernel.org/pub/linux/network/connman/%{name}-%{version}.tar.xz
# Source0-md5:	72cd18041abb17997b32fe6df6b52f5c
URL:		http://connman.net/
BuildRequires:	dbus-devel
BuildRequires:	glib-devel
BuildRequires:	gnutls-devel
BuildRequires:	iptables-devel
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	ppp-devel
BuildRequires:	systemd-devel
Requires(preun,post,postun):	systemd-units
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libppp-plugin.so.*

%description
The ConnMan project provides a daemon for managing Internet
connections within embedded devices running the Linux operating
system. The Connection Manager is designed to be slim and to use as
few resources as possible, so it can be easily integrated. It is a
fully modular system that can be extended, through plug-ins, to
support all kinds of wired or wireless technologies. Also,
configuration methods, like DHCP and domain name resolving, are
implemented using plug-ins. The plug-in approach allows for easy
adaption and modification for various use cases.

%package vpn
Summary:	VPN daemon
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description vpn
VPN support for ConnMan.

%package devel
Summary:	Header files for ConnMan plugins
Group:		Development/Libraries

%description devel
Header files for ConnMan plugins.

%prep
%setup -q

%build
%configure \
	L2TP=/usr/sbin/xl2tpd			\
	PPPD=/usr/sbin/pppd			\
	PPTP=/usr/sbin/pptp			\
	WPASUPPLICANT=/usr/sbin/wpa_supplicant	\
	--disable-silent-rules			\
	--enable-hh2serial-gps			\
	--enable-iospm				\
	--enable-l2tp				\
	--enable-nmcompat			\
	--enable-openconnect			\
	--enable-openvpn			\
	--enable-polkit				\
	--enable-pptp				\
	--enable-threads			\
	--enable-tist				\
	--enable-vpnc				\
	--with-openconnect=/usr/sbin/openconnect	\
	--with-openvpn=/usr/sbin/openvpn	\
	--with-vpnc=/usr/bin/vpnc		\
	--with-systemdunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/connman/{plugins*,scripts}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post connman.service

%preun
%systemd_preun connman.service

%postun
%systemd_postun

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/connmand
%dir %{_libdir}/connman
%dir %{_libdir}/connman/plugins
%attr(755,root,root) %{_libdir}/connman/plugins/hh2serial-gps.so
%attr(755,root,root) %{_libdir}/connman/plugins/iospm.so
%attr(755,root,root) %{_libdir}/connman/plugins/tist.so
%dir %{_libdir}/connman/scripts
%attr(755,root,root) %{_libdir}/connman/scripts/libppp-plugin.so*
/etc/dbus-1/system.d/connman.conf
/etc/dbus-1/system.d/connman-nmcompat.conf
/usr/share/polkit-1/actions/net.connman.policy
%{systemdunitdir}/connman.service

%files vpn
%defattr(644,root,root,755)
%dir %{_libdir}/connman/plugins-vpn
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/l2tp.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/openconnect.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/openvpn.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/pptp.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/vpnc.so
%attr(755,root,root) %{_libdir}/connman/scripts/openconnect-script
%attr(755,root,root) %{_libdir}/connman/scripts/openvpn-script
%attr(755,root,root) %{_sbindir}/connman-vpnd
%{_datadir}/dbus-1/system-services/net.connman.vpn.service
%{_datadir}/polkit-1/actions/net.connman.vpn.policy
%{_sysconfdir}/dbus-1/system.d/connman-vpn-dbus.conf
%{systemdunitdir}/connman-vpn.service

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%{_includedir}/connman
%{_pkgconfigdir}/connman.pc

