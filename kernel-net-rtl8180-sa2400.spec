#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rtl8180_ver	0.20.2
%define		_rtl8180_name	rtl8180
%define		_rel		0.1
Summary:	Linux driver for WLAN cards based on rtl8180
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie rtl8180
Name:		kernel-net-rtl8180
Version:	%{_rtl8180_ver}
Release:	%{_rel}
Group:		Base/Kernel
License:	GPL v2
Source0:	http://dl.sourceforge.net/rtl8180-sa2400/%{_rtl8180_name}-%{_rtl8180_ver}.tar.gz
# Source0-md5:	53270a6b0d9df24c17d833c37a829dd5
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
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie rtl8180.

Ten pakiet zawiera modu� j�dra Linuksa UP.

%package -n kernel-smp-net-rtl8180
Summary:	Linux SMP driver for WLAN cards based on rtl8180
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych opartych na uk�adzie rtl8180
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel-smp}

%description -n kernel-smp-net-rtl8180
This is a Linux driver for WLAN cards based on rtl8180.

This package contains Linux SMP module.

%description -n kernel-smp-net-rtl8180 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk�adzie rtl8180.

Ten pakiet zawiera modu� j�dra Linuksa SMP.

%prep
%setup -q -n %{_rtl8180_name}-%{_rtl8180_ver}

%build
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/include/linux/version.h include/linux/version.h
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		M=$PWD O=$PWD \
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