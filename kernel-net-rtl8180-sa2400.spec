#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rtl8180_ver	0.21
%define		_rtl8180_name	rtl8180
%define		_rel		5
Summary:	Linux driver for WLAN cards based on rtl8180
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie rtl8180
Name:		kernel-net-rtl8180-sa2400
Version:	%{_rtl8180_ver}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
License:	GPL
Source0:	http://dl.sourceforge.net/rtl8180-sa2400/%{_rtl8180_name}-%{_rtl8180_ver}.tar.gz
# Source0-md5:	11f24f693f9661a8bef0305ace663e4a
Patch0:		%{name}-kernel-2.6.12.patch
URL:		http://rtl8180-sa2400.sourceforge.net
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on rtl8180.

This package contains Linux UP module.

%description -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie rtl8180.

Ten pakiet zawiera modu³ j±dra Linuksa UP.

%package -n kernel-smp-net-rtl8180
Summary:	Linux SMP driver for WLAN cards based on rtl8180
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych opartych na uk³adzie rtl8180
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel-smp}

%description -n kernel-smp-net-rtl8180
This is a Linux driver for WLAN cards based on rtl8180.

This package contains Linux SMP module.

%description -n kernel-smp-net-rtl8180 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie rtl8180.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{_rtl8180_name}-%{_rtl8180_ver}

%patch0 -p1

%build
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o KSRC=$PWD/o\
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		M=$PWD O=$PWD/o KSRC=$PWD/o\
		%{?with_verbose:V=1}
	for i in ieee80211-r8180 ieee80211_crypt-r8180 ieee80211_crypt_wep-r8180 \
		r8180; do
		mv $i{,-$cfg}.ko
	done
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
for i in ieee80211-r8180 ieee80211_crypt-r8180 ieee80211_crypt_wep-r8180 \
	r8180; do
install $i-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$i.ko
done
%if %{with smp} && %{with dist_kernel}
for i in ieee80211-r8180 ieee80211_crypt-r8180 ieee80211_crypt_wep-r8180 \
	r8180; do
install $i-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/$i.ko
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post -n kernel-smp-net-rtl8180
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-rtl8180
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-rtl8180
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
