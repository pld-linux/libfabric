# TODO:
# - xpmem support (--enable-xpmem, https://github.com/hpc/xpmem)
# - cuda support
# - gdrcopy (https://github.com/NVIDIA/gdrcopy, requires cuda)
# - level_zero (--with-ze, https://github.com/oneapi-src/level-zero + libdrm-devel)
# - AWS Neuron (--with-neuron, nrt/nrt.h)
# - lttng (--with-lttng, BR: lttng-ust-devel)
# - psm2 (https://github.com/cornelisnetworks/opa-psm2)
# - rocr (https://github.com/RadeonOpenCompute/ROCR-Runtime)
# - SynapseAI (--with-synapseai, habanalabs/synapse_api.h)
# - ucx (http://www.openucx.org/)
# - proprietary providers (cxi...)
#
# Conditional build:
%bcond_without	opx	# OPX provider
%bcond_with	psm2	# PSM2 provider
%bcond_without	psm3	# PSM3 provider
#
%ifnarch %{x8664} aarch64
# structures are full of assumptions about 64-bit [u]intptr_t and size_t
%undefine	with_opx
%endif
%ifnarch %{x8664} x32
%undefine	with_psm2
%undefine	with_psm3
%endif
Summary:	User-space RDMA Fabric interface library
Summary(pl.UTF-8):	Biblioteka interfejsu przestrzeni użytkownika RDMA Fabric
Name:		libfabric
Version:	1.22.0
Release:	1
License:	BSD or GPL v2
Group:		Libraries
#Source0Download: https://github.com/ofiwg/libfabric/releases
Source0:	https://github.com/ofiwg/libfabric/releases/download/v%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	b2c8c4092b29a2e1bc08c617846c2427
URL:		https://github.com/ofiwg/libfabric
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
# for efa, psm3, usnic, verbs
BuildRequires:	libibverbs-devel >= 31
# for usnic
BuildRequires:	libnl-devel >= 3.2
%if %{with psm2}
BuildRequires:	libpsm2-devel
%endif
# for verbs
BuildRequires:	librdmacm-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	liburing-devel >= 2.1
%if %{with opx} || %{with psm3}
BuildRequires:	libuuid-devel
%endif
%if %{with opx} || %{with psm3}
# for psm2, psm3
BuildRequires:	numactl-devel
%endif
Conflicts:	fabtests < 1.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfabric provides a user-space API to access high-performance fabric
services, such as RDMA.

%description -l pl.UTF-8
libfabric dostarcza API przestrzeni użytkownika pozwalające na dostęp
do wysoko wydajnych usług sieci typu fabric, takich jak RDMA.

%package devel
Summary:	Development files for libfabric library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libfabric
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libibverbs-devel
Requires:	libnl-devel >= 3.2
Requires:	librdmacm-devel

%description devel
Header files for libfabric library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libfabric.

%package static
Summary:	Static libfabric library
Summary(pl.UTF-8):	Statyczna biblioteka libfabric
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libfabric library.

%description static -l pl.UTF-8
Statyczna biblioteka libfabric.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_opx:--disable-opx} \
	%{!?with_psm2:--disable-psm2} \
	%{!?with_psm3:--disable-psm3} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfabric.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS.md README
%attr(755,root,root) %{_bindir}/fi_info
%attr(755,root,root) %{_bindir}/fi_pingpong
%attr(755,root,root) %{_bindir}/fi_strerror
%attr(755,root,root) %{_libdir}/libfabric.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfabric.so.1
%{_mandir}/man1/fi_info.1*
%{_mandir}/man1/fi_pingpong.1*
%{_mandir}/man1/fi_strerror.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfabric.so
%{_includedir}/rdma/fabric.h
%{_includedir}/rdma/fi_*.h
%{_includedir}/rdma/providers
%{_pkgconfigdir}/libfabric.pc
%{_mandir}/man3/fi_*.3*
%{_mandir}/man7/fabric.7*
%{_mandir}/man7/fi_*.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libfabric.a
