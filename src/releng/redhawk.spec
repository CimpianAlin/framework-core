#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK core.
#
# REDHAWK core is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

%{!?_ossiehome:  %define _ossiehome  /usr/local/redhawk/core}
%{!?_sdrroot:    %define _sdrroot    /var/redhawk/sdr}
%define _prefix %{_ossiehome}
Prefix:         %{_ossiehome}
Prefix:         %{_sdrroot}
Prefix:         %{_sysconfdir}

%define groupname redhawk
%define username redhawk

Name:           redhawk
Version:        1.9.1
Release:        0.1%{?dist}
Summary:        REDHAWK is a Software Defined Radio framework

Group:          Applications/Engineering
License:        LGPLv3+
URL:            http://redhawksdr.org/
Source:         %{name}-%{version}.tar.gz
Vendor:         REDHAWK

# BuildRoot required for el5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

# el6 gives us issues with rpaths
%if 0%{?rhel} == 6
%define __arch_install_post %{nil}
%endif

%if 0%{?rhel} >= 6
Requires:       util-linux-ng
%else
Requires:       e2fsprogs
%endif
Requires:       java >= 1.6
Requires:       python
Requires:       numpy
Requires:       libomniorbpy

%if 0%{?rhel} >= 6
BuildRequires:  libuuid-devel
BuildRequires:  boost-devel = 1.41.0
%else
BuildRequires:  e2fsprogs-devel
BuildRequires:  boost141-devel
%endif
BuildRequires:  autoconf automake libtool
BuildRequires:  expat-devel
BuildRequires:  java-devel >= 1.6
BuildRequires:  python-devel >= 2.4
BuildRequires:  log4cxx-devel >= 0.10
BuildRequires:  omniORB-devel >= 4.1.0
BuildRequires:  libomniorbpy-devel >= 3.6
BuildRequires:  libomniEvents2-devel
BuildRequires:  xsd >= 3.3.0

%description
REDHAWK is a Software Defined Radio framework.
 * Commit: __REVISION__
 * Source Date/Time: __DATETIME__

%package sdrroot-dom-mgr
Summary:        SDRROOT Domain Manager
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
Provides:       DomainManager = %{version}-%{release}

%description sdrroot-dom-mgr
The SDDROOT Domain Manager software package

%package sdrroot-dom-profile
Summary:        Basic domain manager profile
Group:          Applications/Engineering
Requires:       %{name}-sdrroot-dom-mgr = %{version}-%{release}

%description sdrroot-dom-profile
A generic domain profile and domain profile template

%package sdrroot-dev-mgr
Summary:        SDRROOT Device Manager
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
Provides:       DeviceManager = %{version}-%{release}

%description sdrroot-dev-mgr
The SDDROOT Device Manager software package

%package devel
Summary:        The REDHAWK development package
Group:          Applications/Engineering

# REDHAWK
Requires:       redhawk = %{version}-%{release}

# Base dependencies
%if 0%{?rhel} >= 6
Requires:       libuuid-devel
Requires:       boost-devel = 1.41.0
%else
Requires:       e2fsprogs-devel
Requires:       boost141-devel
%endif
Requires:       autoconf automake libtool
Requires:       log4cxx-devel >= 0.10

# omniORB / omniORBpy
Requires:       omniORB-devel >= 4.1.0
Requires:       libomniorbpy-devel >= 3.6

# Languages
Requires:       gcc-c++
Requires:       python-devel >= 2.4
Requires:       java-devel >= 1.6

# qtbrowse
Requires:       PyQt

%description devel
This package ensures that all requirements for REDHAWK development are installed. It also provides a useful development utilities.


%prep
%setup -q


%build
# build the core framework
cd src
./reconf
%configure --with-sdr=%{_sdrroot} --with-pyscheme=home
make %{?_smp_mflags}


%install
rm -rf --preserve-root $RPM_BUILD_ROOT

# install ossie framework
cd src
make install DESTDIR=$RPM_BUILD_ROOT
cp control/sdr/domain/DomainManager.dmd.xml $RPM_BUILD_ROOT%{_sdrroot}/dom/domain/


%clean
rm -rf --preserve-root $RPM_BUILD_ROOT


%pre
groupadd -r -f %{groupname}
if id %{username} &> /dev/null; then
  echo "%{username} user account exists and will not be added"
else
  /usr/sbin/useradd -M -r -s /sbin/nologin \
    -c "REDHAWK System Account" -n -g %{groupname} %{username} > /dev/null
fi


%files
%defattr(-,root,root,-)
%{_bindir}
%exclude %{_bindir}/qtbrowse
%exclude %{_bindir}/prf2py.py
%exclude %{_bindir}/py2prf
%dir %{_includedir}
%dir %{_prefix}/lib
%ifarch x86_64
%dir %{_prefix}/lib64
%endif
%{_prefix}/lib/CFInterfaces.jar
%{_prefix}/lib/apache-commons-lang-2.4.jar
%{_prefix}/lib/log4j-1.2.15.jar
%{_prefix}/lib/ossie.jar
%{_prefix}/lib/python
%exclude %{_prefix}/lib/python/ossie/apps/qtbrowse
%{_libdir}/libomnijni.so.0
%{_libdir}/libomnijni.so.0.0.0
%{_libdir}/libossiecf.so.3
%{_libdir}/libossiecf.so.3.0.0
%{_libdir}/libossiecfjni.so.0
%{_libdir}/libossiecfjni.so.0.0.0
%{_libdir}/libossieidl.so.3
%{_libdir}/libossieidl.so.3.0.0
%{_libdir}/libossieparser.so.2
%{_libdir}/libossieparser.so.2.0.0
%dir %{_libdir}/pkgconfig
%{_datadir}
%{_sysconfdir}/profile.d/redhawk.csh
%{_sysconfdir}/profile.d/redhawk.sh
%{_sysconfdir}/ld.so.conf.d/redhawk.conf

%files sdrroot-dom-mgr
%defattr(664,%{username},%{groupname})
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dom
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dom/components
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dom/domain
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dom/mgr
%attr(775,%{username},%{groupname}) %{_sdrroot}/dom/mgr/DomainManager
%{_sdrroot}/dom/mgr/*.xml
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dom/waveforms
%attr(644,root,root) %{_sysconfdir}/profile.d/redhawk-sdrroot.csh
%attr(644,root,root) %{_sysconfdir}/profile.d/redhawk-sdrroot.sh

%files sdrroot-dom-profile
%defattr(664,%{username},%{groupname})
%config %{_sdrroot}/dom/domain/DomainManager.dmd.xml
%{_sdrroot}/dom/domain/DomainManager.dmd.xml.template

%files sdrroot-dev-mgr
%defattr(664,%{username},%{groupname})
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dev
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dev/devices
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dev/mgr
%attr(2775,%{username},%{groupname}) %dir %{_sdrroot}/dev/nodes
%attr(775,%{username},%{groupname}) %{_sdrroot}/dev/mgr/DeviceManager
%{_sdrroot}/dev/mgr/DeviceManager.*
%attr(644,root,root) %{_sysconfdir}/profile.d/redhawk-sdrroot.csh
%attr(644,root,root) %{_sysconfdir}/profile.d/redhawk-sdrroot.sh

%files devel
%defattr(-,root,root,-)
%{_bindir}/qtbrowse
%{_bindir}/prf2py.py
%{_bindir}/py2prf
%{_includedir}/ossie
%{_libdir}/libomnijni.*a
%{_libdir}/libomnijni.so
%{_libdir}/libossiecf.*a
%{_libdir}/libossiecf.so
%{_libdir}/libossiecfjni.*a
%{_libdir}/libossiecfjni.so
%{_libdir}/libossieidl.so
%{_libdir}/libossieidl.*a
%{_libdir}/libossieparser.*a
%{_libdir}/libossieparser.so
%{_libdir}/pkgconfig/ossie.pc
%{_prefix}/lib/python/ossie/apps/qtbrowse


%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%changelog
* Tue Apr 18 2013 1.9.0-1
- Re-work lots of dependencies
- Package for REDHAWK development
- Minor fixes for docs, licensing
- Explicitly require Java for build

* Tue Mar 12 2012 - 1.8.3-4
- Update licensing information
- Add URL for website
- Change group to a standard one, per Fedora
- Remove standard build dependencies

* Mon Sep 19 2011 - 1.7.2-2
- Further split RPMs to allow more granularity in installations

* Tue Jun 07 2011 - 1.7.0-0
- Split sdrroot into -dev and dom
- Attempt to fully capture Requires and BuildRequires
- Stop packaging components into SDRROOT

* Tue Jan 11 2011 - 1.6.0-0
- Initial spec file for redhawk and redhawk-sdrroot.
# end of file
