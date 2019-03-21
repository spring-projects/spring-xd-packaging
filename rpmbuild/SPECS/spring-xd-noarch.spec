# Spring-XD spec file for RHEL 6

Name:           spring-xd 
Version:        1.3.2.RELEASE
Release:        1
Summary:        Pivotal Spring XD: One stop solution to simplify Big Data complexity
# see /usr/share/doc/rpm-*/GROUPS for list
Group:          Applications/Databases
License:        Apache License v2.0
Vendor:         Pivotal
Packager:       spring-xd@pivotal.io
URL:            https://projects.spring.io/spring-xd

# Disable automatic dependency processing
#####AutoReqProv: no

%define GROUP_NAME      pivotal
%define USER_NAME       spring-xd
%define USER_GECOS      "Spring-XD User"
%define USER_HOME_BASE	/opt/pivotal
%define USER_HOME	%{USER_HOME_BASE}/%{USER_NAME}
%define INSTALL_DIR     /opt/pivotal/spring-xd
# install dir with slash escapes for use in sed
%define INSTALL_DIR_ESC     \\\/opt\\\/pivotal\\\/spring-xd
%define INIT_FILE_ADMIN       spring-xd-admin
%define INIT_FILE_CONTAINER    spring-xd-container
%define SYSCONFIG_FILE    spring-xd

Source0:        spring-xd-%{version}-dist.zip
# init scripts
Source1:        %{INIT_FILE_ADMIN}
Source2:        %{INIT_FILE_CONTAINER}
Source3:        %{SYSCONFIG_FILE}

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  

Requires: chkconfig

%description
Pivotal's Spring XD is a unified, distributed, and extensible system for data
ingestion, real time analytics, batch processing, and data export. The
project's goal is to simplify the development of big data applications.


%prep
# setup, disable unpacking, create dir with name-version
# setup cmd for non-compiling pkgs
%setup -T -c %{name}-%{version}
# can prep into the build directory by doing

if [ ! -z %{_builddir} ]; then
   echo "BUILDDIR: %{_builddir}"
   # clean out the builddir
   rm -rf %{_builddir}/*
fi
echo "DEBUG: %{_builddir}"
cd %{_builddir}
###gzip -dc %{SOURCE0} | tar -xf -
unzip %{SOURCE0} 
if [ $? -ne 0 ]; then
  exit $?
fi


#cp %{_sourcedir}/%{patch} %{_builddir}/%{name}-%{version}
cp -p %SOURCE1 .
cp -p %SOURCE2 .
cp -p %SOURCE3 .


###%build

%pre

# create group and user account if they do not exist
if [ ! -n "`/usr/bin/getent group %{GROUP_NAME}`" ]; then
    %{_sbindir}/groupadd -r %{GROUP_NAME} 2> /dev/null
fi

if [ ! -n "`/usr/bin/getent passwd %{USER_NAME}`" ]; then
    # Do not attempt to create a home dir at this point in the RPM install
    # because the parent dirs do not yet exist and we can't be certain 
    # about /home
    %{_sbindir}/useradd -c %{USER_GECOS} -r -g %{GROUP_NAME} -M %{USER_NAME} 2> /dev/null
fi

%install
echo "entering install"
rm -rf %{buildroot}
mkdir -p %{buildroot}%{INSTALL_DIR}-%{version}

# remove redis src
rm -rf %{_builddir}/%{name}-%{version}/redis
# remove windows bat files
rm -f %{_builddir}/%{name}-%{version}/xd/bin/*.bat
rm -f %{_builddir}/%{name}-%{version}/gemfire/bin/*.bat
rm -f %{_builddir}/%{name}-%{version}/shell/bin/*.bat


cp -rp %{_builddir}/%{name}-%{version}/* %{buildroot}%{INSTALL_DIR}-%{version}/

mkdir -p %{buildroot}%{INSTALL_DIR}-%{version}/xd/logs
touch %{buildroot}%{INSTALL_DIR}-%{version}/xd/logs/admin.log
touch %{buildroot}%{INSTALL_DIR}-%{version}/xd/logs/container.log
mkdir -p %{buildroot}%{INSTALL_DIR}-%{version}/xd/data/jobs

mkdir -p %{buildroot}/etc/rc.d/init.d
cp -p %{_builddir}/%{INIT_FILE_ADMIN} %{buildroot}/etc/rc.d/init.d/
cp -p %{_builddir}/%{INIT_FILE_CONTAINER} %{buildroot}/etc/rc.d/init.d/

mkdir -p %{buildroot}/etc/sysconfig
cp -p %{_builddir}/%{SYSCONFIG_FILE} %{buildroot}/etc/sysconfig/


%clean
####echo "entering clean"

%files
####echo "entering files"

%defattr(-, %{USER_NAME}, %{GROUP_NAME} -)
%{INSTALL_DIR}-%{version}

%ghost %{INSTALL_DIR}-%{version}/xd/logs/admin.log
%ghost %{INSTALL_DIR}-%{version}/xd/logs/container.log

%attr(755, root, root) /etc/rc.d/init.d/*
%config(noreplace) %attr(644, root, root) /etc/sysconfig/%{SYSCONFIG_FILE}

%post

# Check if this RPM is presently installed, if so, none of this should be needed
if [ "$1" = "1" ]; then

   # configure chkconfig
   chkconfig --add %{INIT_FILE_ADMIN}
   chkconfig --add %{INIT_FILE_CONTAINER}

   # add softlink
   ln -s %{INSTALL_DIR}-%{version} %{INSTALL_DIR}
   ln -s %{INSTALL_DIR}/shell/bin/xd-shell %{_bindir}/xd-shell

fi # end if for RPM not presently installed


%preun
# If we are doing an erase
if [ "$1" = "0" ]; then
   # stop proc
   service %{INIT_FILE_CONTAINER} stop > /dev/null
   service %{INIT_FILE_ADMIN} stop > /dev/null

   # remove from chkconfig
   chkconfig --del %{INIT_FILE_CONTAINER}
   chkconfig --del %{INIT_FILE_ADMIN}
   
   # remove old log files
   rm -f %{INSTALL_DIR}-%{version}/xd/logs/{admin,container}.log.*

fi

# $1 == 1 @ upgrade, $1 == 0 @ uninstall
%postun
if [ "$1" = "0" ]; then
   # remove softlinks
   rm -f %{INSTALL_DIR}
   rm -f %{_bindir}/xd-shell
   # remove this logfile
   rm -f /tmp/spring.log
elif [ "$1" = "1" ]; then
   # On upgrade, remove the old version softlink
   rm -f %{INSTALL_DIR}
fi

# Always passed 0
%posttrans
   # This is the final scriptlet to run during an upgrade and runs from the
   # new package
   # remove the old softlink
   rm -f %{INSTALL_DIR}
   # Add the new softlink
   ln -s %{INSTALL_DIR}-%{version} %{INSTALL_DIR}
