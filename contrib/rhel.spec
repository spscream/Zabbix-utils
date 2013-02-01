%define name python-zabbix-utils
%define version 0.1
%define unmangled_version 0.1
%define release 1

%define python_sitelib %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib()')

Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Summary: Python zabbix utils for working with zabbix API.

Group: Applications/System
License: GPLv2
URL: http://auto.ru
Source0: python-zabbix-utils-%{unmangled_version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

BuildRequires: python-devel
BuildRequires: python-setuptools
Requires: python-setuptools
Requires: python-argparse
Requires: python-configobj
Requires: GitPython

%description
Zabbix utils is a python module for working with Zabbix API.
With it you can:
- Create and update hostgroup graphs by key;
- Create and update graphs for items with key matched pattern;
- Mass create of items and graphs.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build \
    --root "%{buildroot}"

    %clean
    %{__rm} -rf %{buildroot}

    %files
    %defattr(-, root, root, 0755)
    %{_bindir}/*
    %{python_sitelib}/*

    %changelog
    * Wed Jan 30 2013 Alexander Malaev <scream@spuge.net> - 0.2.8
    - Initial package
