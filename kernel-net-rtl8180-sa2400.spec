#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rtl8180_name	rtl8180
%define		_rel		6
Summary:	Linux driver for WLAN cards based on rtl8180
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie rtl8180
%define		_specname	kernel-net-rtl8180-sa2400
Name:		kernel%{_alt_kernel}-net-rtl8180-sa2400
Version:	0.21
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/rtl8180-sa2400/%{_rtl8180_name}-%{version}.tar.gz
# Source0-md5:	11f24f693f9661a8bef0305ace663e4a
Patch0:		%{_specname}-kernel-2.6.12.patch
Patch1:		%{_specname}-module-params.patch
Patch2:		%{_specname}-2.6.20.patch
URL:		http://rtl8180-sa2400.sourceforge.net
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
%{?with_dist_kernel:%requires_releq_kernel}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel%{_alt_kernel}}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on rtl8180.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
rtl8180.

%prep
%setup -q -n %{_rtl8180_name}-%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p1

cat > Makefile << EOF
obj-m += r8180.o ieee80211-r8180.o ieee80211_crypt-r8180.o ieee80211_crypt_wep-r8180.o 

r8180-objs := r8180_core.o r8180_sa2400.o r8180_93cx6.o r8180_wx.o r8180_max2820.o r8180_gct.o
ieee80211-r8180-objs := ieee80211_rx.o ieee80211_tx.o ieee80211_wx.o ieee80211_module.o
ieee80211_crypt-r8180-objs := ieee80211_crypt.o
ieee80211_crypt_wep-r8180-objs := ieee80211_crypt_wep.o

CFLAGS += -DCONFIG_MODULE_NAME_SOME_OPTION=1
%{?debug:CFLAGS += -DCONFIG_MODULE_NAME_DEBUG=1}
EOF

%build
%build_kernel_modules -m ieee80211-r8180,ieee80211_crypt-r8180,ieee80211_crypt_wep-r8180,r8180

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m ieee80211-r8180,ieee80211_crypt-r8180 -d kernel/drivers/net/wireless
%install_kernel_modules -m ieee80211_crypt_wep-r8180,r8180 -d kernel/drivers/net/wireless

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*
