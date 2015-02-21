#
# Conditional build:
%bcond_with	psm	# infinipath-psm provider
#
%ifnarch %{ix86} %{x8664}
%undefine	with_psm
%endif
Summary:	User-space RDMA Fabric interface library
Summary(pl.UTF-8):	Biblioteka interfejsu przestrzeni użytkownika RDMA Fabric
Name:		libfabric
%define	subver	rc1
Version:	1.0.0
Release:	1
License:	BSD or GPL v2
Group:		Libraries
Source0:	https://www.openfabrics.org/downloads/ofi/%{name}-%{version}-%{subver}.tar.bz2
# Source0-md5:	aea309fefa9a3ef40f935a647bfa1691
Patch0:		%{name}-missing.patch
URL:		https://github.com/ofiwg/libfabric
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.11
%{?with_psm:BuildRequires:	infinipath-psm-devel >= 3.1}
BuildRequires:	libibverbs-devel
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	librdmacm-devel
BuildRequires:	libtool >= 2:2
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
%setup -q -n %{name}-%{version}-%{subver}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_psm:--disable-psm} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libfabric.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfabric.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfabric.so
%{_libdir}/libfabric.la
%{_includedir}/rdma/fabric.h
%{_includedir}/rdma/fi_*.h
%{_mandir}/man3/fi_*.3*
%{_mandir}/man7/fabric.7*
%{_mandir}/man7/fi_direct.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libfabric.a
